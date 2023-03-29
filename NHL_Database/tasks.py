"""
Defines tasks related to scraping which should be performed.

The scope of tasks is what and how to do, not when - that is handled separately by scheduler module.
"""

import logging
from NHL_Database import data_parser, models


logger = logging.getLogger(__name__)

# from celery.utils.log import get_task_logger
#
# logger = get_task_logger(__name__)

def init_db(x, y):
    tables = ([cls.__name__ for cls in models.__subclasses__()])
    for table in tables:
        model = getattr(models, table)
        model.objects.all().delete()
        class_ = f'{table}Parser'
        parser_class = getattr(data_parser, class_)
        parser = parser_class()
        parser.process_data()


def parse_table(data):
    """
    Parses table data anew. If there are for any reason old data in table, they are deleted for consistency.
    :param data:
    :return:
    """
    table = data['table']
    class_ = f'{table}Parser'
    parser_class = getattr(data_parser, class_)
    parser = parser_class()
    parser.new_data()


def update_table(data):
    # start_time = datetime.datetime.now()
    # table = data['table']
    # update_params = data['update_params']
    # remove_records = data['remove_records']
    # model = getattr(models, table)
    # model.objects.filter(remove_records).all().delete()
    # class_ = f'{table}Parser'
    # parser_class = getattr(data_parser, class_)
    # parser = parser_class()
    # parser.update_data()
    # parser.records.save()
    # models.TableState.update_table_state(table, start_time)
    table = data['table']
    logger.info(f'updating table {table}.')
    class_ = f'{table}Parser'
    parser_class = getattr(data_parser, class_)
    parser = parser_class()
    parser.update_data(data)

def init_tables():
    """
    Check config if all tables have been initialized. If not, initialize them.
    :return:
    """
    models.TableState.init_tables()
    table_state = models.TableState.objects.all()
    for table in table_state:
        print(f'processing table: {table.model_name}')
        process_table(table)


def process_table(table_state):
    """
    Loop through table config and process tables which are not initialized.
    :param config:
    :param table:
    :return:
    """
    if table_state.last_update is None:
        print(f'parsing table: {table_state.model_name} starts')
        parse_table({'table': table_state.model_name})
        print(f'parsing table: {table_state.model_name} ends')
    else:
        # update_table({'table': table_state.model_name})
        pass


def daily_check():
    """
    Perform update of relavant data on daily basis.
    :return:
    """
    logger.info('daily check starts.')
    season = models.Seasons.get_current()
    data_parser.TeamstatsParser().update_data(season=season)
