from db.Database import Database
from config.config import config
from processing.anonymize.Anonymize import anonymize_data
from logging import Logger


def main():
    cfg = config()
    logger = Logger(name="main_logger")
    db = Database(cfg.read('database'))

    anonymize_data(db, logger)


if __name__ == "__main__":
    main()

