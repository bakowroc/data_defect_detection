from db.database import database
from config.config import config
from db.models.RawDataModel import RawDataModel


def main():
    cfg = config()
    db = database(cfg.read('database'))
    data, error = db.get_all("raw_data")

    if error is not None:
        print(error)
        exit(0)

    for row in data:
        raw_data = RawDataModel()
        raw_data.apply(row)

        print(raw_data)


if __name__ == "__main__":
    main()

