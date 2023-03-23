from django.urls import reverse
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APITestCase
import Stats.views as views
import NHL_Database.models as models

class Test_query_filter_seasons(TestCase):

    def test_both_dates(self):
        query = models.Teamstats.objects
        viewset = views.StatsViewSet()
        params = {'season_start': '20002001',
                  'season_end': '20102011'}
        query = viewset.query_filter_seasons(params, query)
        x = str(query.query.where)
        self.assertEqual(x, '(AND: Range(Col(NHL_Database_teamstats, NHL_Database.Teamstats.season), [20002001, 20102011]))')

    def test_start_date(self):
        query = models.Teamstats.objects
        viewset = views.StatsViewSet()
        params = {'season_start': '20002001',
                  'season_end': '-'}
        query = viewset.query_filter_seasons(params, query)
        x = str(query.query.where)
        self.assertEqual(x, '(AND: IntegerGreaterThanOrEqual(Col(NHL_Database_teamstats, NHL_Database.Teamstats.season), 20002001))')

    def test_end_date(self):
        query = models.Teamstats.objects
        viewset = views.StatsViewSet()
        params = {'season_start': '-',
                  'season_end': '20002001'}
        query = viewset.query_filter_seasons(params, query)
        x = str(query.query.where)
        self.assertEqual(x, '(AND: LessThanOrEqual(Col(NHL_Database_teamstats, NHL_Database.Teamstats.season), 20002001))')
