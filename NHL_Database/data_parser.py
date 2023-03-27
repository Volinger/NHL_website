"""
Processes scraped data and parses them to database. Combines scraping and database modules.
"""

from NHL_Database import models
import NHL_Database.scrapers as Scraping
import logging

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

    def update_data(self, **params):
        """
        Updates subset of data based on params
        :return:
        """
        pass


class SeasonsParser(Parser):
    def __init__(self):
        super().__init__()
        self.Scraper = Scraping.Seasons()
        self.Table = models.Seasons

    def parse_data_to_table(self, data):
        for index, record in enumerate(data):
            entry = self.Table(id=index, season=record['seasonId'], games=record['numberOfGames'])
            entry.save()
        logger.info('Successfully parsed seasons.')


class TeamsParser(Parser):
    def __init__(self):
        super().__init__()
        self.Scraper = Scraping.Teams()
        self.Table = models.Teams

    def process_data(self):
        years = [year['season'] for year in models.Seasons.objects.values('season')]
        for year in years:
            data = self.Scraper.get_data(season=year)
            self.parse_data_to_table(data)
            logger.info(f'Successfully parsed teams for season: {year}.')

    def parse_data_to_table(self, data):
        for team in data['teams']:
            entry = self.Table(id=team['id'],
                               team=team['name'],
                               firstYearOfPlay=team['firstYearOfPlay'],
                               active=team['active'])
            entry.save()


class TeamstatsParser(Parser):
    def __init__(self):
        super().__init__()
        self.Scraper = Scraping.TeamStats()
        self.Table = models.Teamstats

    def process_data(self):
        for year in get_all_seasons():
            for team in get_all_teams():
                data = self.Scraper.get_data(season=year, team=team)
                self.parse_data_to_table(data, team, year)
            logger.info(f'Parsed team stats for season: {year}.')

    def parse_data_to_table(self, data, team, season):
        record = self.Table()
        if len(data['stats'][0]['splits']) == 1:    # If there are no data for split == team did not play that season.
            for param, value in data['stats'][0]['splits'][0]['stat'].items():
                setattr(record, param, value)
            # rdb.set_trace()
            record.season_id = season
            record.team_id = team
            record.save()


class PlayersParser(Parser):
    def __init__(self):
        super().__init__()
        self.Scraper = Scraping.Players()
        self.Table = models.Players

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
        if years is None:
            years = get_all_seasons()
        if teams is None:
            teams = get_all_teams()
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
        for player in all_players:
            data = self.Scraper.get_data(player_id=player)
            self.parse_data_to_table(data)

    def parse_data_to_table(self, data):
        record = self.Table()
        record.id = data['id']
        record.lastName = data['lastName']
        record.firstName = data['firstName']
        record.nationality = data['nationality']
        record.primaryPosition = data['primaryPosition']['code']
        record.save()


class SkaterSeasonStatsParser(Parser):

    def __init__(self):
        super().__init__()
        self.Scraper = Scraping.PlayerYearByYearStats()
        self.Table = models.SkaterSeasonStats

    def update_data(self, **params):
        season = params.get('season', None)
        models.SkaterSeasonStats.objects.filter(season=season).delete()

    def process_data(self, **params):
        players = models.Players.objects.filter(primaryPosition__in=['R', 'L', 'C', 'D']).all()
        for player in players:
            all_season_stats = self.Scraper.get_data(player_id=player.id)
            for season_stats in all_season_stats['stats'][0]['splits']:
                if season_stats['league']['name'] == 'National Hockey League':
                    record = self.Table()
                    for param, value in season_stats['stat'].items():
                        setattr(record, param, value)
                    record.powerPlayTimeOnIce = self.convert_time_to_float(record.powerPlayTimeOnIce)
                    record.evenTimeOnIce = self.convert_time_to_float(record.evenTimeOnIce)
                    record.timeOnIce = self.convert_time_to_float(record.timeOnIce)
                    record.shortHandedTimeOnIce = self.convert_time_to_float(record.shortHandedTimeOnIce)
                    record.player = player.id
                    record.season = season_stats['season']
                    team = models.Teams.objects.filter(team=season_stats['team']['name']).values(
                        'id')
                    record.team = team[0]['id']
                    record.save()
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
