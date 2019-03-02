import click

from api.api import server
from config.APPConfig import APPConfig
from create_acronym_map.create_acronym_map import create_acronym_map
from create_data_set_map.create_data_set_map import create_data_set_map
from db.Database import Database
from load_data.load_data import load_data


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


@cli.command('server')
def __server():
    server()



