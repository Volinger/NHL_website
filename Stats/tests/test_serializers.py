from django.test import TestCase
import Stats.serializers as serializers
import NHL_Database.models as models


class Test_PlayersSerializer(TestCase):
    def setUp(self):
        self.attr = {
            'id': 1,
            'primaryPosition': 'D',
            'nationality': 'CAN',
            'firstName': 'John',
            'lastName': 'Connor',
        }

        self.instance = models.Players.objects.create(**self.attr)
        self.serializer = serializers.PlayersSerializer(self.instance)

    def test_serialized_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(self.attr.keys()))

    def test_fields_value(self):
        data = self.serializer.data
        self.assertEqual(set(data.values()), set(self.attr.values()))


class SkaterSeasonStatsSerializer(TestCase):
    def setUp(self):
        self.attr = {
            'season': models.Seasons(season=20002001, games=80),
            'player': models.Players(firstName='John', lastName='Connor', nationality='CAN', primaryPosition='D'),
            'team': models.Teams(team='NSH', firstYearOfPlay=1900, active=True),
            'games': 80,
            'assists': 1,
            'goals': 2,
            'points': 3,
            'plusMinus': 4,
            'shots': 5,
            'hits': 6,
            'powerPlayGoals': 7,
            'powerPlayPoints': 8,
            'powerPlayTimeOnIce': 9.123,
            'evenTimeOnIce': 10.123,
            'penaltyMinutes': 11.123,
            'faceOffPct': 12.123,
            'shotPct': 13.123,
            'gameWinningGoals': 14,
            'overTimeGoals': 15,
            'shortHandedGoals': 16,
            'shortHandedPoints': 17,
            'shortHandedTimeOnIce': 18,
            'blocked': 19,
            'shifts': 20,
            'timeOnIce': 21.123,
        }

        self.instance = models.SkaterSeasonStats.objects.create(**self.attr)
        self.serializer = serializers.SkaterSeasonStatsSerializer(self.instance)

    def test_serialized_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(self.attr.keys()))

    def test_fields_value(self):
        data = self.serializer.data
        self.assertEqual(set(data.values()), set(self.attr.values()))
