from db.database import database
from config.config import config


def main():
    cfg = config()
    db = database(cfg.read('database'))
    data = db.execute_query("SELECT * FROM raw_data")

    for row in data:
        print(row.id)


if __name__ == "__main__":
    main()
