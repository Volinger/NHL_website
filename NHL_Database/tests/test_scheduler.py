import datetime

import NHL_Database.scheduler as scheduler
from django.test import TestCase
import os
import json

class Test_update_scraping_config(TestCase):

    def setUp(self):
        self.config = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_Scraping_config.json')
        with open(self.config, 'w') as cfg:
            test_data = json.dumps({
                "seasons": None,
                "dummy": "2000-01-02 01:02:03"
            })
            cfg.write(test_data)

    # def test_update(self):
    #     table_state = m
    #     started = str(datetime.datetime(year=2000, month=1, day=1, hour=0, minute=0, second=0))
    #     scheduler.update_table_state(self.config, started, table='seasons')
    #     with open(self.config) as cfg:
    #         data = json.load(cfg)
    #     expected = {
    #         "seasons": '2000-01-01 00:00:00',
    #         "dummy": "2000-01-02 01:02:03"
    #     }
    #     self.assertEqual(expected, data)

    def tearDown(self):
        os.remove(self.config)
