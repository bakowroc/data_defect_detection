from db.models.DataPoint import DataPoint
from db.models.DataSetMap import DataSetMap
from db.models.Operator import Operator


def count_dataset(limit=700):
    result = DataSetMap.objects.all()

    for data_set_map in result:
        operator_id = data_set_map.operator_id
        acronym = data_set_map.acronym
        kpi_name = data_set_map.kpi_name
        has_enough = len(DataPoint.objects.filter(operator_id=operator_id, acronym=acronym, kpi_name=kpi_name).limit(limit))
        DataSetMap.objects(operator_id=operator_id, acronym=acronym, kpi_name=kpi_name).update(has_enough=has_enough >= limit)

        operator = Operator.objects(operator_id=operator_id).first()
        if not operator.has_enough or operator.has_enough is None:
            print(operator_id, has_enough >= limit)
            Operator.objects(operator_id=operator_id).update(has_enough=has_enough >= limit)

