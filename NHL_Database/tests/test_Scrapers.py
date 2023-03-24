"""
The tests located here are related to NHL API. Since retrieving the data takes long time (for some Scrapers it can take
hours), the convention is to check only single endpoint for each scraper and compare single record.
Purpose here is only to test that the API has same format as in the past.
"""

from django.test import TestCase
import NHL_Database.scrapers as scrapers


class Test_Seasons(TestCase):

    def setUp(self):
        self.expected = {
            'conferencesInUse': False,
            'divisionsInUse': False,
            'numberOfGames': 22,
            'olympicsParticipation': False,
            'regularSeasonEndDate': '1918-03-06',
            'regularSeasonStartDate': '1917-12-19',
            'seasonEndDate': '1918-03-30',
            'seasonId': '19171918',
            'tiesInUse': True,
            'wildCardInUse': False}

    def test_data(self):
        scraper = scrapers.Seasons()
        result = scraper.get_data()
        self.assertEqual(result[0], self.expected)


class Test_Teams(TestCase):

    def setUp(self):
        self.expected = {
            'id': 1,
            'name': 'New Jersey Devils',
            'firstYearOfPlay': '1982',
            'active': True
        }

    def test_data(self):
        scraper = scrapers.Teams()
        data = scraper.get_data(season=20002001)['teams'][0]
        keys = ['id', 'name', 'firstYearOfPlay', 'active']
        result = {key: value for key, value in data.items() if key in keys}
        self.assertEqual(result, self.expected)
