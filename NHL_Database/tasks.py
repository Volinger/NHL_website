from celery import shared_task
import time
from NHL_Database import Data_Parser, models


# from celery.utils.log import get_task_logger
#
# logger = get_task_logger(__name__)

@shared_task
def add(x, y):
    time.sleep(2)
    return x + y


@shared_task
def init_db(x, y):
    tables = ([cls.__name__ for cls in models.__subclasses__()])
    for table in tables:
        model = getattr(models, table)
        model.objects.all().delete()
        class_ = f'{table}Parser'
        parser_class = getattr(Data_Parser, class_)
        parser = parser_class()
        parser.process_data()


@shared_task
def parse_table(data):
    table = data['table']
    model = getattr(models, table)
    model.objects.all().delete()
    class_ = f'{table}Parser'
    parser_class = getattr(Data_Parser, class_)
    parser = parser_class()
    parser.process_data()

@shared_task
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
