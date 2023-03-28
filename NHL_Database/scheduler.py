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
import NHL_Database.models as models

def start():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("127.0.0.1", 47200))
    except socket.error:
        pass
    else:
        print('starting')
        scheduler = BackgroundScheduler()
        scheduler.add_job(init_tables)
        scheduler.start()

def init_tables():
    """
    Check config if all tables have been initialized. If not, initialize them.
    This is run before regular checking scheduler is launched.
    :return:
    """
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Scraping_config.json')
    table_state = models.TableState.objects.all()
    for table in table_state:
        print(f'processing table: {table_state.table}')
        process_table(table)
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(daily_check, trigger='cron', hour=8)
    # scheduler.start()


def process_table(config_path, table_state, table):
    """
    Loop through table config and process tables which are not initialized.
    :param config:
    :param table:
    :return:
    """
    if table_state.last_update is None:
        start_time = datetime.datetime.now()
        print(f'parsing table: {table} starts')
        tasks.parse_table({'table': table})
        print(f'parsing table: {table} ends')
        models.TableState.update_table_state(table_state.table, start_time)


def daily_check():
    """
    Perform update of relavant data on daily basis.
    :return:
    """
    season = models.Seasons.get_current()
    for table in ['Players', 'Teamstats', 'SkaterSeasonStats']:
        tasks.parse_table(data={'table': table, 'seasons': [season]})




