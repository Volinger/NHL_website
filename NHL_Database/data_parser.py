"""
Processes scraped data and parses them to database. Combines scraping and database modules.

There are two basic options when this module is used:
1. When tables are empty and need to be filled with initial data. This is handler by parser's new_data() method.
2. When tables are already filled, but need to be updated. This is handler by parser's update_data() method.
"""

from NHL_Database import models
import NHL_Database.scrapers as Scraping
import logging
from django.db.transaction import atomic
import datetime

logger = logging.getLogger(__name__)

def get_all_seasons():
    years = [year['season'] for year in models.Seasons.objects.values('season')]
    return years


def get_all_teams():
    teams = [team['id'] for team in models.Teams.objects.values('id')]
    return teams


class ParserHandler:

    def parse_all_empty_tables(self):
        for child in self.get_all_parsers():
            table = eval(child)()
            if table.table_empty(table.Table):
                table.process_data()

    def get_all_parsers(self):
        all_subclasses = ([cls.__name__ for cls in Parser.__subclasses__()])
        return all_subclasses


class Parser:
    """
    Interface for parser classes
    """

    def __init__(self):
        self.data = None
        self.Scraper: Scraping.BaseScraper = None
        self.Table = None

    def new_data(self):
        """
        Defines how to process data if table is empty.
        :return:
        """
        pass

    def update_data(self, **params):
        """
        Defines how to process data if table contains some data but needs to be updated.
        :return:
        """
        pass

    def add_record(self, record):
        record.save()

    def update_table_state(self, update_time):
        models.TableState.update_table_state(self.Table, update_time)

    def process_data(self):
        """
        1. get data
        2. parse to db
        3. save
        :return:
        """
        data = self.Scraper.get_data()
        self.parse_data_to_table(data)

    def parse_data_to_table(self, data):
        """
        Parse processed data to DB.
        :return:
        """
        pass

    def convert_time_to_float(self, time):
        if time is None:
            return time
        time_values = time.split(":")
        result = float(time_values[0]) + float(time_values[1])/60
        return result


class SeasonsParser(Parser):
    def __init__(self):
        super().__init__()
        self.Scraper = Scraping.Seasons()
        self.Table = models.Seasons

    def parse_data_to_table(self, data):
        for index, record in enumerate(data):
            record = self.Table(id=index, season=record['seasonId'], games=record['numberOfGames'])
            self.add_record(record)
        logger.info('Successfully parsed seasons.')

    @atomic
    def new_data(self):
        start_time = datetime.datetime.now()
        self.Table.objects.all().delete()
        self.process_data()
        # self.Table.bulk_create(self.records)
        models.TableState.update_table_state(self.Table._meta.object_name, start_time)

    def update_data(self, **params):
        """
        For seasons, there is only one endpoint, update is same as parsing all data.
        :param params:
        :return:
        """
        self.process_data()


class TeamsParser(Parser):
    def __init__(self):
        super().__init__()
        self.Scraper = Scraping.Teams()
        self.Table = models.Teams

    @atomic
    def new_data(self):
        start_time = datetime.datetime.now()
        self.Table.objects.all().delete()
        years = get_all_seasons()
        self.process_data(years=years)
        # self.Table.bulk_create(self.records)
        models.TableState.update_table_state(self.Table._meta.object_name, start_time)

    def update_data(self, **params):
        self.process_data(years=params['season'])

    def process_data(self, years=None):
        for year in years:
            data = self.Scraper.get_data(season=year)
            self.parse_data_to_table(data)
            logger.info(f'Successfully parsed teams for season: {year}.')

    def parse_data_to_table(self, data):
        for team in data['teams']:
            record = self.Table(id=team['id'],
                               team=team['name'],
                               firstYearOfPlay=team['firstYearOfPlay'],
                               active=team['active'])
            self.add_record(record)

class TeamstatsParser(Parser):
    def __init__(self):
        super().__init__()
        self.Scraper = Scraping.TeamStats()
        self.Table = models.Teamstats

    @atomic
    def new_data(self):
        start_time = datetime.datetime.now()
        self.Table.objects.all().delete()
        years = get_all_seasons()
        self.process_data(years=years)
        # self.Table.bulk_create(self.records)
        models.TableState.update_table_state(self.Table._meta.object_name, start_time)

    @atomic
    def update_data(self, **params):
        logger.info(f'Started Teamstats update for season: {params["season"]}.')
        start_time = datetime.datetime.now()
        self.Table.objects.filter(season=params['season']).all().delete()
        logger.info(f'Removed old records for season: {params["season"]}.')
        self.process_data(years=[params['season']])
        models.TableState.update_table_state(self.Table._meta.object_name, start_time)


    def process_data(self, years=None):
        for year in years:
            for team in get_all_teams():
                data = self.Scraper.get_data(season=year, team=team)
                self.parse_data_to_table(data, team, year)
            logger.info(f'Parsed team stats for season: {year}.')

    def parse_data_to_table(self, data, team, season):
        record = self.Table()
        if len(data['stats'][0]['splits']) == 1:    # If there are no data for split == team did not play that season.
            for param, value in data['stats'][0]['splits'][0]['stat'].items():
                setattr(record, param, value)
            record.season_id = season
            record.team_id = team
            self.add_record(record)


class PlayersParser(Parser):
    def __init__(self):
        super().__init__()
        self.Scraper = Scraping.Players()
        self.Table = models.Players

    @atomic
    def new_data(self):
        start_time = datetime.datetime.now()
        self.Table.objects.all().delete()
        years = get_all_seasons()
        teams = get_all_teams()
        self.process_data(years=years, teams=teams)
        # self.Table.bulk_create(self.records)
        models.TableState.update_table_state(self.Table._meta.object_name, start_time)

    def update_data(self, **params):
        seasons = params.get('seasons', None)
        teams = params.get('teams', None)
        self.process_data(years=seasons, teams=teams)

    def process_data(self, years=None, teams=None):
        """
        Processes every team roster in every season and reads all the players on rosters.
        :return:
        """
        all_players = []
        team_roster_scraper = Scraping.SeasonTeamRoster()
        for year in years:
            for team in teams:
                roster_data = team_roster_scraper.get_data(team=team, season=year)
                try:
                    roster = roster_data['teams'][0]['roster']['roster']
                    players = [player['person']['id'] for player in roster]
                    all_players += players
                except KeyError:
                    pass
            logger.info(f'Processed player stats for season: {year}.')
        all_players = set(all_players)
        logger.info(f'Players: {all_players}.')
        for index, player in enumerate(all_players):
            logger.info(f'processing player {index} / {len(all_players)}')
            data = self.Scraper.get_data(player_id=player)
            self.parse_data_to_table(data)
        logger.info(f'Processed all players')

    def parse_data_to_table(self, data):
        record = self.Table()
        record.id = data['id']
        record.lastName = data['lastName']
        record.firstName = data['firstName']
        record.nationality = data['nationality']
        record.primaryPosition = data['primaryPosition']['code']
        self.add_record(record)


class SkaterSeasonStatsParser(Parser):

    def __init__(self):
        super().__init__()
        self.Scraper = Scraping.PlayerYearByYearStats()
        self.Table = models.SkaterSeasonStats

    @atomic
    def new_data(self):
        start_time = datetime.datetime.now()
        self.Table.objects.all().delete()
        players = models.Players.objects.filter(primaryPosition__in=['R', 'L', 'C', 'D']).all()
        self.process_data(year=None, players=players, single_season=False)
        # self.Table.bulk_create(self.records)
        models.TableState.update_table_state(self.Table._meta.object_name, start_time)

    @atomic
    def update_data(self, **params):
        # TBD process only players which are active.
        season = params.get('season', None)
        players = models.Players.objects.filter(primaryPosition__in=['R', 'L', 'C', 'D']).all()
        self.process_data(year=season, players=players, single_season=True)

    def process_data(self, year=None, players=None, single_season=None):
        for index, player in enumerate(players):
            all_season_stats = self.Scraper.get_data(player_id=player.id)
            for season_stats in all_season_stats['stats'][0]['splits']:
                self.process_single_player(player, season_stats, single_season, year)
            logger.info(f'Processed season stats {index} / {len(players)}')

    def process_single_player(self, player, season_stats, single_season, year):
        if not single_season or season_stats['season'] == year:
            if season_stats['league']['name'] == 'National Hockey League':
                record = self.Table()
                for param, value in season_stats['stat'].items():
                    setattr(record, param, value)
                record.powerPlayTimeOnIce = self.convert_time_to_float(record.powerPlayTimeOnIce)
                record.evenTimeOnIce = self.convert_time_to_float(record.evenTimeOnIce)
                record.timeOnIce = self.convert_time_to_float(record.timeOnIce)
                record.shortHandedTimeOnIce = self.convert_time_to_float(record.shortHandedTimeOnIce)
                record.player_id = player.id
                record.season_id = season_stats['season']
                team = models.Teams.objects.filter(team=season_stats['team']['name']).values(
                    'id')
                record.team_id = team[0]['id']
                self.add_record(record)
    #
# class GoalieSeasonStats(Parser):
#     def __init__(self):
#         super().__init__()
#         self.Scraper = Scraping.PlayerYearByYearStats()
#         self.Table = Db.GoalieSeasonStats
#
#     def process_data(self):
#         players = self.DB_Handler.get_records(Db.Players, primaryPosition='G')
#         for player in players:
#             all_season_stats = self.Scraper.get_data(player_id=player.id)
#             for season_stats in all_season_stats['stats'][0]['splits']:
#                 if season_stats['league']['name'] == 'National Hockey League':
#                     record = self.Table()
#                     for param, value in season_stats['stat'].items():
#                         setattr(record, param, value)
#                     record.timeOnIce = self.convert_time_to_float(record.timeOnIce)
#                     record.player_id = player.id
#                     record.season_id = self.DB_Handler.get_records(Db.Seasons, season=season_stats['season'])[0].id
#                     record.team_id = self.DB_Handler.get_records(Db.Teams, team=season_stats['team']['name'])[0].id
#                     self.DB_Handler.add_record(record)
