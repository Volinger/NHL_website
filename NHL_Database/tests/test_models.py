from NHL_Database import models
from django.test import TestCase
import datetime

class Test_update_scraping_config(TestCase):
    fixtures = ['test_data.json']

    def setUp(self):
        self.table_name = models.TableState.objects.first().table_name
        self.start_time = datetime.datetime(year=2000, month=1, day=1, hour=0, minute=0, second=0)

    def test_update(self):
        models.TableState.update_table_state(self.table_name, self.start_time)
        self.assertEqual(models.TableState.objects.first().start_time, self.start_time)
