import click

from api.api import server
from config.APPConfig import APPConfig
from count_dataset.count_dataset import count_dataset
from create_acronym_map.create_acronym_map import create_acronym_map
from create_data_set_map.create_data_set_map import create_data_set_map
from db.Database import Database
from load_data.load_data import load_data
from load_data.load_operators import load_operators


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


@cli.command('count_dataset')
def __count_dataset():
    count_dataset()


@cli.command('server')
def __server():
    server()



