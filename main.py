import argparse, sys

from db.Database import Database
from config.config import config
from processing.anonymize.anonymize_data import get_anonymized_data
from logging import Logger

from processing.prepare_tables import prepare_info_tables


parser=argparse.ArgumentParser()
parser.add_argument('--withReparse', help='Run program and parse anonymization data to new table')
parser.add_argument('--createTables', help='Run program and fill with data additional tables')

args=parser.parse_args()


def main():
    cfg = config()
    logger = Logger(name="main_logger")
    db = Database(cfg.read('database'))

    value_data_list, kpi_definitions = get_anonymized_data(db, logger, with_reparse=args.withReparse)

    if args.createTables:
        prepare_info_tables(db, value_data_list)

    print("-> Starting data processing")


if __name__ == "__main__":
    main()

