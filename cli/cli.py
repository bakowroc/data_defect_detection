import click
import time_uuid

from api.api import server
from config.APPConfig import APPConfig
from create_acronym_map.create_acronym_map import create_acronym_map
from create_data_set_map.create_data_set_map import create_data_set_map
from db.Database import Database
from db.models.DataPoint import DataPoint
from load_data.load_data import load_data
from load_data.load_operators import load_operators
from outlier_detector.OutlierDetector import OutlierDetector


@click.group()
def cli():
    cfg = APPConfig()
    Database(cfg.read("database"))


@cli.command('create_acronym_map')
def __create_acronym_map():
    create_acronym_map()


@cli.command('create_data_set_map')
def __create_data_set_map():
    create_data_set_map()


@cli.command('load_data')
def __load_data():
    load_data()


@cli.command('load_operators')
def __load_operators():
    load_operators()


@cli.command('test_outlier')
def __test_outlier():
    operator_id = 987
    acronym = "PILSRUNDALE"
    kpi_name = "MGWO_1122"
    parsed_result = []
    result = DataPoint.objects.filter(operator_id=operator_id, acronym=acronym, kpi_name=kpi_name)

    for data_point in result:
        parsed_result.append({
            'value': data_point.value,
            'date': str(time_uuid.TimeUUID.convert(data_point.date).get_datetime()),
            'timestamp': time_uuid.TimeUUID.convert(data_point.date).get_timestamp()
        })

    detector = OutlierDetector(dataset=parsed_result)
    reconstruction = detector.knn_mean_sliding(n_clusters=50)

    print(len(reconstruction))


@cli.command('server')
def __server():
    server()



