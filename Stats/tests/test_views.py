from django.urls import reverse
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APITestCase
import Stats.views as views
import NHL_Database.models as models
from rest_framework.test import APIClient


class Test_query_filter_seasons(TestCase):

    def test_both_dates(self):
        query = models.Teamstats.objects
        viewset = views.StatsViewSet()
        params = {'season_start': '20002001', 'season_end': '20102011'}
        query = viewset.query_filter_seasons(params, query)
        x = str(query.query.where)
        self.assertEqual(x, '(AND: Range(Col(NHL_Database_teamstats, NHL_Database.Teamstats.season), [20002001, 20102011]))')

    def test_start_date(self):
        query = models.Teamstats.objects
        viewset = views.StatsViewSet()
        params = {'season_start': '20002001'}
        query = viewset.query_filter_seasons(params, query)
        x = str(query.query.where)
        self.assertEqual(x, '(AND: IntegerGreaterThanOrEqual(Col(NHL_Database_teamstats, NHL_Database.Teamstats.season), 20002001))')

    def test_end_date(self):
        query = models.Teamstats.objects
        viewset = views.StatsViewSet()
        params = {'season_end': '20002001'}
        query = viewset.query_filter_seasons(params, query)
        x = str(query.query.where)
        self.assertEqual(x, '(AND: LessThanOrEqual(Col(NHL_Database_teamstats, NHL_Database.Teamstats.season), 20002001))')


class Test_standings(TestCase):

    def test_response(self):
        client = APIClient()
        response = client.get(reverse('Stats-standings'), {}, format='json')
        self.assertEqual(response.status_code, 200)


class Test_skater_stats(TestCase):

    def test_response(self):
        client = APIClient()
        response = client.get(reverse('Stats-skater-stats'), {}, format='json')
        self.assertEqual(response.status_code, 200)


class Test_player_career(TestCase):

    def test_response(self):
        client = APIClient()
        response = client.get(reverse('Stats-player-career'), {"player_id": 1}, format='json')
        self.assertEqual(response.status_code, 200)
