from NHL_Database import models
from django.test import TestCase
import datetime
import pytz

class Test_update_table_state(TestCase):
    fixtures = ['test_data.json']

    def setUp(self):
        self.model_name = models.TableState.objects.first().model_name
        self.start_time = datetime.datetime(year=2000, month=1, day=1, hour=0, minute=0, second=0, tzinfo=pytz.UTC)

    def test_update(self):
        models.TableState.update_table_state(self.model_name, self.start_time)
        last_update = models.TableState.objects.first().last_update
        self.assertEqual(last_update, self.start_time)


class Test_init_tables(TestCase):
    fixtures = ['test_data.json']

    def setUp(self):
        self.models = ['Seasons', 'Teams', 'Teamstats', 'Players', 'SkaterSeasonStats'].sort()

    def test_init(self):
        models.TableState.init_tables()
        created_models = [model['model_name'] for model in models.TableState.objects.values('model_name')].sort()
        self.assertEqual(self.models, created_models)
