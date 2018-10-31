import re
from datetime import datetime, timedelta
from processing.anonymize.DataFilter import filter_complex_kpis, filter_not_matched_data
from processing.anonymize.DataReparser import kpi_definitions_map
from numpy import array_split
import matplotlib.pyplot as plt


def anonymize_data(db, logger):
    kpis = process_raw_kpis(db ,logger)
    kpi_names = get_names(kpis)
    raw_data = process_raw_data(db, logger, kpi_names)

    dates = list(map(lambda row: row.date, raw_data))
    values = list(map(lambda row: row.value, raw_data))

    plt.figure(num=None, figsize=(24, 10), dpi=300, facecolor='w', edgecolor='k')
    plt.plot(dates, values)
    plt.show()


def process_raw_kpis(db, logger):
    raw_kpis, error = db.get_all("kpi_defs")
    if error: logger.error(error)

    filtered_kpis = filter_complex_kpis(raw_kpis)
    parsed_kpis = []

    for kpi in filtered_kpis:
        mapped_kpi = kpi_definitions_map(kpi)
        parsed_kpis.append(mapped_kpi)

    mapped_kpis = parsed_kpis

    #Insert into DB

    return mapped_kpis


def process_raw_data(db, logger, kpi_names):
    dates = generate_days(datetime(2018, 1, 1, 0, 0, 0), datetime.now())
    mapped_raw_data = []

    for chunk_dates in dates:
        raw_data, error = db.get_by_dates('raw_data', chunk_dates)
        if error:
            logger.error(error)

        for row in raw_data:
            filtered_row = filter_not_matched_data(row, kpi_names)
            # Map row
            mapped_raw_data.append(filtered_row)


    # Insert into DB
    return list(filter(lambda row: row is not None, mapped_raw_data))


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
        kpi_name = re.search('\[(.*)\]', kpi['formula'])
        kpi_names.append(kpi_name.group(1))

    return kpi_names
