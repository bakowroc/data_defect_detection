from db.models.DataSetMap import DataSetMap
from db.models.DataPoint import DataPoint
from db.models.AcronymNameMap import AcronymNameMap


def create_data_set_map():
    if len(AcronymNameMap.objects.limit(1)) is 0:
        raise ResourceWarning("collection acronym_name_map is empty")

    if len(DataPoint.objects.limit(1)) is 0:
        raise ResourceWarning("collection data_points is empty")

    data_points_keys = []

    def func(data_point):
        keys = (data_point.operator_id, data_point.kpi_name, data_point.acronym)
        if keys not in data_points_keys:
            data_points_keys.append(keys)
            operator_id = keys[0]
            kpi_name = keys[1]
            acronym = keys[2]
            DataSetMap.create(operator_id=operator_id, acronym=acronym, kpi_name=kpi_name)

    DataPoint.run_per_each(func)


