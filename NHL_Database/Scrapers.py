"""
This module allows scraping of NHL.com API.
API documentation: https://gitlab.com/dword4/nhlapi/-/blob/master/stats-api.md

Usage:
Instantiate specific endpoint which you would like to scrape, along with any **kwargs used by the endpoint, i.e.
data = Seasons(year=2022). API will return data in JSON format, unless specified otherwise.

Some endpoints require additional parameters (i.e. team stats require season for which data are requested). Since
these data are provided by other endpoints, either provide data manually or scrape prerequisite endpoints first.
"""

import requests
from abc import abstractmethod

class BaseScraper:
    """
    Interface for data scraping classes.
    """

    base_endpoint = ""
    endpoint = ""

    def get_data(self, **kwargs):
        self.finalize_endpoint(**kwargs)
        self.data = requests.get(self.endpoint).json()
        self.remove_copyright()
        self.filter_data()
        return self.data

    def remove_copyright(self):
        """
        This section is present in all known API so far, remove it since it is not useful for scraping purposes.
        :return:
        """
        if 'copyright' in self.data:
            self.data.pop('copyright')

    def filter_data(self):
        pass

    def finalize_endpoint(self, **kwargs):
        """
        If endpoint can contain additional parameters process them and append to url in child classes in this method.
        :param kwargs:
        :return:
        """
        self.endpoint = self.base_endpoint

class Seasons(BaseScraper):
    """
    List of all NHL seasons.
    """
    base_endpoint = "https://statsapi.web.nhl.com/api/v1/seasons"

    def filter_data(self):
        self.data = self.data['seasons']
        # self.data = [season['seasonId'] for season in self.data]


class Teams(BaseScraper):
    """
    Info about Teams
    """
    base_endpoint = "https://statsapi.web.nhl.com/api/v1/teams"

    def finalize_endpoint(self, **kwargs):
        self.endpoint = f'{self.base_endpoint}?season={kwargs["season"]}'


class TeamStats(BaseScraper):
    """
    Team stats for individual seasons.
    :param team, season, default = current_season
    """
    base_endpoint = "https://statsapi.web.nhl.com/api/v1/teams"

    def finalize_endpoint(self, **kwargs):
        self.endpoint = f'{self.base_endpoint}/{kwargs["team"]}/stats'
        self.endpoint = f'{self.endpoint}?season={kwargs["season"]}'


class SeasonTeamRoster(BaseScraper):
    """
    Team Roster for given season.
    """
    base_endpoint = "https://statsapi.web.nhl.com/api/v1/teams"

    def finalize_endpoint(self, **kwargs):
        self.endpoint = f'{self.base_endpoint}/{kwargs["team"]}?expand=team.roster'
        self.endpoint = f'{self.endpoint}&season={kwargs["season"]}'


class Players(BaseScraper):
    """
    List of players.
    """
    base_endpoint = "https://statsapi.web.nhl.com/api/v1/people"

    def finalize_endpoint(self, **kwargs):
        self.endpoint = f'{self.base_endpoint}/{kwargs["player_id"]}'

    def filter_data(self):
        self.data = self.data['people'][0]

class PlayerYearByYearStats(BaseScraper):
    """
    Stats for every season of player's career.
    """
    base_endpoint = "https://statsapi.web.nhl.com/api/v1/people"

    def finalize_endpoint(self, **kwargs):
        self.endpoint = f'{self.base_endpoint}/{kwargs["player_id"]}/stats?stats=yearByYear'
