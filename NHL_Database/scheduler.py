"""
Scraping of data needs to be done in specific intervals in order to make sure that database is up-to-date.
This module handles scheduling of tasks when necessary.
In order to ensure data integrity, configuration is used to track what state is specific table in (= last time scraping
was performed). This configuration is updated when tasks are successfully performed and data saved to database.
Each scraping task should be handled as a single transaction on DB level, so that updates of data match configuration.
This ensures that even if server gets down during execution of scraping task, the scraping can continue normally after
restart.
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from .something_update import update_something
import sys, socket
import time, datetime
import json
import os
import NHL_Database.tasks as tasks

def start():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("127.0.0.1", 47200))
    except socket.error:
        pass
    else:
        scheduler = BackgroundScheduler()
        scheduler.add_job(init_tables)
        scheduler.start()
        print('eest')

def init_tables():
    """
    Check config if all tables have been initialized. If not, initialize them.
    This is run before regular checking scheduler is launched.
    :return:
    """
    config = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Scraping_config.json')
    with open(config, 'r') as cfg:
        table_config = json.load(cfg)
    for table in table_config:
        process_table(config, table)
    time.sleep(5)
    scheduler = BackgroundScheduler()
    scheduler.add_job(schedule_updates, trigger='interval', seconds=5)
    scheduler.start()
    pass


def process_table(config, table):
    if table is None:
        starttime = datetime.datetime.now()
        parsing_successful = tasks.parse_table(table)
        if parsing_successful:
            update_scraping_config(config, starttime, table)


def update_scraping_config(config, starttime, table):
    with open(config, 'r') as cfg:
        table_config = json.load(cfg)
        table_config[table] = starttime
        result = json.dumps(table_config)
    with open(config, 'w') as cfg:
        cfg.write(result)


def schedule_updates():
    """
    Schedule updates of tables in regular intervals.
    :return:
    """