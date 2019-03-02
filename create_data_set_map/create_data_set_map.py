from db.models.DataSetMap import DataSetMap
from db.models.RawDataPoint import RawDataPoint
from db.models.AcronymNameMap import AcronymNameMap
from utils.date import generate_months, generate_days


def create_data_set_map():
    if len(AcronymNameMap.objects.limit(1)) is 0:
        raise ResourceWarning("collection acronym_name_map is empty")

    if len(RawDataPoint.objects.limit(1)) is 0:
        raise ResourceWarning("collection raw_data_point is empty")

    data_point_keys = []

    def func(raw_data_point):
        data_point_keys.append((raw_data_point.cord_id, raw_data_point.kpi_basename, raw_data_point.acronym))

    RawDataPoint.run_per_each(func)

    for keys in list(set(data_point_keys)):
        operator_id = keys[0]
        kpi_name = keys[1]
        acronym = AcronymNameMap.get(raw_acronym=keys[2]).acronym
        DataSetMap.create(operator_id=operator_id, acronym=acronym, kpi_name=kpi_name)


