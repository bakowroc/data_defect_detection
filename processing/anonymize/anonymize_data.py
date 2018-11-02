import re
from datetime import datetime, timedelta
from logging import Logger
from typing import List

from db.models.KpiDefinition import KpiDefinition
from db.models.ValueData import ValueData
from processing.anonymize.data_filter import filter_complex_kpis, filter_not_matched_data
from numpy import array_split


from processing.anonymize.NameMapper import NameMapper


def get_anonymized_data(db, logger: Logger, with_reparse = False) -> (List[ValueData], List[KpiDefinition]):
    if with_reparse:
        print("-> Reparse requested. Anonymization started")

        kpis = process_raw_kpis(db ,logger)
        value_data_list = process_raw_data(db, logger, get_names(kpis))

        print("Inserted {} rows".format(len(value_data_list)))
        return value_data_list, kpis

    print("-> Getting anonymized data directly from DB")
    kpis = get_all_kpi_definitions(db)
    value_data_list = get_all_value_data(db)
    return value_data_list, kpis


def process_raw_kpis(db, logger) -> List[KpiDefinition]:
    print("Process raw kpis started")

    raw_kpis, error = db.get_all("kpi_defs")
    if error: logger.error(error)

    filtered_kpis = filter_complex_kpis(raw_kpis)
    parsed_kpis = []

    for kpi_definition in filtered_kpis:
        mapped_kpi_definition = KpiDefinition(
            definition_id=kpi_definition.definition_id,
            formula=kpi_definition.formula,
            date=kpi_definition.date,
            tags=kpi_definition.tags,
            technology=kpi_definition.technology,
            unit=kpi_definition.unit
        )

        db.execute_query(mapped_kpi_definition.insert())
        parsed_kpis.append(mapped_kpi_definition)

    return parsed_kpis


def process_raw_data(db, logger, kpi_names) -> List[ValueData]:
    print("Process raw data started")

    name_mapper = NameMapper()
    dates = generate_days(datetime(2014, 1, 1, 0, 0, 0), datetime.now())
    data = []

    for index, chunk_dates in enumerate(dates):
        print("Processing chunk between ({}, {}) | {}/{}. ".format(chunk_dates[0], chunk_dates[-1], index + 1, len(dates)))

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

    return data


def generate_days(start_date, end_date) -> List[List[datetime]]:
    days = []
    delta = end_date - start_date  # timedelta

    for i in range(delta.days + 1):
        day = start_date + timedelta(i)
        days.append(str(day))

    return array_split(days, len(days) / 30)


def get_names(kpis) -> List[str]:
    kpi_names = []

    for kpi in kpis:
        kpi_name = re.search('\[(.*)\]', kpi.formula)
        kpi_names.append(kpi_name.group(1))

    return kpi_names


def get_all_value_data(db) -> List[ValueData]:
    dates = generate_days(datetime(2014, 1, 1, 0, 0, 0), datetime.now())
    value_data_list = []

    for chunk_dates in dates:
        db_result, error = db.get_by_dates('value_data', chunk_dates)
        result_list = list(db_result)
        if len(result_list):
            value_data_chunk = list(map(lambda value_data: ValueData(cassandra_row=value_data) , result_list))
            value_data_list += value_data_chunk

    return list(filter(None, value_data_list))


def get_all_kpi_definitions(db) -> List[KpiDefinition]:
    db_result, error = db.get_all('kpi_definitions')
    return list(map(lambda kpi_definition: KpiDefinition(cassandra_row=kpi_definition), db_result))