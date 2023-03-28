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
import socket
from .tasks import init_tables


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




