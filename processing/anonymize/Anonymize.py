import re
from datetime import datetime, timedelta
from logging import Logger

from db.models.ValueData import ValueData
from processing.anonymize.DataFilter import filter_complex_kpis, filter_not_matched_data
from numpy import array_split


from processing.anonymize.NameMapper import NameMapper


def anonymize_data(db, logger: Logger):
    print("Anonymization started")

    kpis = process_raw_kpis(db ,logger)
    value_data_list, acronym_map = process_raw_data(db, logger, get_names(kpis))

    print(len(value_data_list))


def process_raw_kpis(db, logger):
    print("Process raw kpis started")

    raw_kpis, error = db.get_all("kpi_defs")
    if error: logger.error(error)

    filtered_kpis = filter_complex_kpis(raw_kpis)
    parsed_kpis = []

    for kpi in filtered_kpis:
        parsed_kpis.append(kpi)

    mapped_kpis = parsed_kpis

    #Insert into DB

    return mapped_kpis


def process_raw_data(db, logger, kpi_names):
    print("Process raw data started")

    name_mapper = NameMapper()
    dates = generate_days(datetime(2014, 1, 1, 0, 0, 0), datetime.now())
    data = []

    for index, chunk_dates in enumerate(dates):
        print("Processing chunk {}/{}".format(index + 1, len(dates)))

        raw_data, error = db.get_by_dates('raw_data', chunk_dates)
        if error: logger.error(error)

        for row in raw_data:
            filtered_row = filter_not_matched_data(row, kpi_names)
            if filtered_row is not None:
                mapped_acronym = name_mapper.map_acronym(filtered_row.acronym)
                value_data = ValueData(
                    operator_id=filtered_row.cord_id,
                    acronym=mapped_acronym,
                    kpi_name=filtered_row.kpi_name,
                    date=filtered_row.date,
                    value=filtered_row.value
                )

                db.execute_query(value_data.insert())
                data.append(value_data)


    return data, name_mapper.acronym_map


def generate_days(start_date, end_date):

    days = []

    delta = end_date - start_date  # timedelta

    for i in range(delta.days + 1):
        day = start_date + timedelta(i)
        days.append(str(day))

    return array_split(days, len(days) / 30)


def get_names(kpis):
    kpi_names = []

    for kpi in kpis:
        kpi_name = re.search('\[(.*)\]', kpi.formula)
        kpi_names.append(kpi_name.group(1))

    return kpi_names
