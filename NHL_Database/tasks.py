import datetime

from NHL_Database import data_parser, models


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
    table = data['table']
    model = getattr(models, table)
    model.objects.all().delete()
    class_ = f'{table}Parser'
    parser_class = getattr(data_parser, class_)
    parser = parser_class()
    parser.process_data()

def update_table(data):
    # table = data['table']
    # update_params = data['update_params']
    # remove_records = data['remove_records']
    # model = getattr(models, table)
    # model.objects.filter(remove_records).all().delete()
    # class_ = f'{table}Parser'
    # parser_class = getattr(Data_Parser, class_)
    # parser = parser_class()
    # parser.process_data()
    pass


def init_tables():
    """
    Check config if all tables have been initialized. If not, initialize them.
    This is run before regular checking scheduler is launched.
    :return:
    """
    models.TableState.init_tables()
    table_state = models.TableState.objects.all()
    for table in table_state:
        print(f'processing table: {table.model_name}')
        process_table(table)
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(daily_check, trigger='cron', hour=8)
    # scheduler.start()


def process_table(table_state):
    """
    Loop through table config and process tables which are not initialized.
    :param config:
    :param table:
    :return:
    """
    if table_state.last_update is None:
        start_time = datetime.datetime.now()
        print(f'parsing table: {table_state.model_name} starts')
        parse_table({'table': table_state.model_name})
        print(f'parsing table: {table_state.model_name} ends')
        models.TableState.update_table_state(table_state.model_name, start_time)


def daily_check():
    """
    Perform update of relavant data on daily basis.
    :return:
    """
    season = models.Seasons.get_current()
    for table in ['Players', 'Teamstats', 'SkaterSeasonStats']:
        parse_table(data={'table': table, 'seasons': [season]})
