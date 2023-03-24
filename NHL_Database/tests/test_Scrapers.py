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


class Test_TeamStats(TestCase):

    def setUp(self):
        self.expected = {
            'gamesPlayed': 82,
            'wins': 48,
            'losses': 19,
            'ot': 3,
            'pts': 111,
            'ptPctg': '67.7',
            'goalsPerGame': 3.598,
            'goalsAgainstPerGame': 2.378,
            'evGGARatio': 1.1969,
            'powerPlayPercentage': '22.9',
            'powerPlayGoals': 71.0,
            'powerPlayGoalsAgainst': 49.0,
            'powerPlayOpportunities': 310.0,
            'penaltyKillPercentage': '84.7',
            'shotsPerGame': 31.5854,
            'shotsAllowed': 24.6829,
            'winScoreFirst': 0.727,
            'winOppScoreFirst': 0.421,
            'winLeadFirstPer': 0.839,
            'winLeadSecondPer': 0.921,
            'winOutshootOpp': 0.583,
            'winOutshotByOpp': 0.684,
            'faceOffsTaken': 5259.0,
            'faceOffsWon': 2597.0,
            'faceOffsLost': 2662.0,
            'faceOffWinPercentage': '49.4',
            'shootingPctg': 11.4,
            'savePctg': 0.904
        }
        
    def test_data(self):
        scraper = scrapers.TeamStats()
        result = scraper.get_data(season=20002001, team=1)['stats'][0]['splits'][0]['stat']
        self.assertEqual(result, self.expected)


class Test_Players(TestCase):

    def setUp(self):
        self.expected = {
            'primaryPosition': 'L',
            'firstName': 'Greg',
            'lastName': 'Adams',
            'nationality': 'CAN'
        }

    def test_data(self):
        scraper = scrapers.Players()
        data = scraper.get_data(player_id=8444894)
        keys = ['firstName', 'lastName', 'nationality']
        result = {key: value for key, value in data.items() if key in keys}
        result['primaryPosition'] = data['primaryPosition']['code']
        self.assertEqual(result, self.expected)
