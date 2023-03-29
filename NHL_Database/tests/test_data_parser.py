from django.test import TestCase
from NHL_Database import data_parser
from NHL_Database import models


class Test_SeasonsParser(TestCase):

    def setUp(self):
        self.parser = data_parser.SeasonsParser()
        self.scraped_data = [{
            "seasonId": "19171918",
            "regularSeasonStartDate": "1917-12-19",
            "regularSeasonEndDate": "1918-03-06",
            "seasonEndDate": "1918-03-30",
            "numberOfGames": 22,
            "tiesInUse": True,
            "olympicsParticipation": False,
            "conferencesInUse": False,
            "divisionsInUse": False,
            "wildCardInUse": False
        }, {
            "seasonId": "19181919",
            "regularSeasonStartDate": "1918-12-21",
            "regularSeasonEndDate": "1919-02-20",
            "seasonEndDate": "1919-03-29",
            "numberOfGames": 18,
            "tiesInUse": True,
            "olympicsParticipation": False,
            "conferencesInUse": False,
            "divisionsInUse": False,
            "wildCardInUse": False
        }]

        self.expected = [
            {
                'id': 0,
                'season': 19171918,
                'games': 22},
            {
                'id': 1,
                'season': 19181919,
                'games': 18}
        ]

    def test_parse_data(self):
        self.parser.parse_data_to_table(self.scraped_data)
        records = list(models.Seasons.objects.values())
        self.assertEqual(records, self.expected)


class Test_TeamsParser(TestCase):

    def setUp(self):
        self.parser = data_parser.TeamsParser()
        self.scraped_data = {
            'teams':
                [{
                    'id': 1,
                    'name': 'New Jersey Devils',
                    'firstYearOfPlay': '1982',
                    'active': True
                }]
        }

        self.expected = [
            {
                "id": 1,
                "team": "New Jersey Devils",
                "firstYearOfPlay": 1982,
                "active": True
            }
        ]
    def test_parse_data(self):
        self.parser.parse_data_to_table(self.scraped_data)
        records = list(models.Teams.objects.values())
        self.assertEqual(records, self.expected)
