from db.Database import Database
from config.config import config
from db.models.RawDataModel import RawDataModel
from processing.anonymize.DataFilter import DataFilter


def main():
    cfg = config()
    db = Database(cfg.read('database'))
    data, error = db.get_all("raw_data")

    if error is not None:
        print(error)
        exit(0)

    kpis, error = db.get_by_fields(
        "kpi_defs",
        ['definition_id', 'formula', 'description', 'unit', 'date', 'technology', 'tags']
    )

    if error is not None:
        print(error)
        exit(0)

    filtered_kpis = DataFilter().filter_complex_kpis(kpis)

    for row in filtered_kpis:
        print(row)



if __name__ == "__main__":
    main()

