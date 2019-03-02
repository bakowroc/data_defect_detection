from typing import List

from cassandra.cqlengine.columns import DateTime
from cassandra.cqlengine.functions import *

from create_acronym_map.NameMapper.NameMapper import NameMapper
from db.models.AcronymNameMap import AcronymNameMap
from db.models.RawDataPoint import RawDataPoint
from utils.date import generate_days, generate_months


def get_acronyms() -> List[str]:
    if len(RawDataPoint.objects.limit(1)) is 0:
        raise ResourceWarning("collection raw_data_points is empty")

    acronyms = []

    def func(raw_data_point):
        acronyms.append(raw_data_point.acronym)

    RawDataPoint.run_per_each(func)

    return list(set(acronyms))


def create_acronym_map():
    name_mapper = NameMapper()

    for acronym in get_acronyms():
        name_mapper.map_value(acronym)

    for raw_acronym, acronym in name_mapper.value_map.items():
        AcronymNameMap.create(raw_acronym=raw_acronym, acronym=acronym)
