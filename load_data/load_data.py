from db.models.AcronymNameMap import AcronymNameMap
from db.models.DataPoint import DataPoint
from db.models.DataSetMap import DataSetMap
from db.models.KpiDefinition import KpiDefinition
from db.models.Operator import Operator
from db.models.RawDataPoint import RawDataPoint
from db.models.RawKpiDefinition import RawKpiDefinition

from utils.date import create_uuid
from utils.kpis import filter_complex_kpis


def load_data():
    load_kpi_definitions()
    load_data_points()
    load_operators()


def load_kpi_definitions(skip_if_exists=True):
    print("Loading kpi_definitions")

    if len(RawKpiDefinition.objects.limit(1)) is 0:
        raise ResourceWarning("collection raw_kpi_definitions is empty")

    if len(KpiDefinition.objects.limit(1)) is not 0 and skip_if_exists:
        print("Skipping due to skip_if_exists: True")
        return

    result = RawKpiDefinition.objects.all()
    filtered_result = filter_complex_kpis(result)
    for raw_kpi_definition in filtered_result:
        d_id = raw_kpi_definition.id
        description = raw_kpi_definition.text
        formula = raw_kpi_definition.formula
        tags = raw_kpi_definition.tags
        technology = raw_kpi_definition.technology
        unit = raw_kpi_definition.unit

        KpiDefinition.create(id=d_id, description=description, formula=formula, tags=tags, technology=technology, unit=unit)


def load_data_points(skip_if_exists=True):
    print("Loading data_points")

    if len(RawDataPoint.objects.limit(1)) is 0:
        raise ResourceWarning("collection raw_data_points is empty")

    if len(AcronymNameMap.objects.limit(1)) is 0:
        raise ResourceWarning("collection acronym_name_map is empty")

    if len(DataPoint.objects.limit(1)) is not 0 and skip_if_exists:
        print("Skipping due to skip_if_exists: True")
        return

    def func(raw_data_point):
        operator_id = raw_data_point.cord_id
        kpi_name = raw_data_point.kpi_basename
        acronym = AcronymNameMap.get(raw_acronym=raw_data_point.acronym).acronym
        date = create_uuid(raw_data_point.date)
        value = raw_data_point.value

        DataPoint.create(operator_id=operator_id, kpi_name=kpi_name, acronym=acronym, date=date, value=value)

    RawDataPoint.run_per_each(func)


def load_operators(skip_if_exists=True):
    print("Loading operators")
    if len(DataSetMap.objects.limit(1)) is 0:
        raise ResourceWarning("collection data_set_map is empty")

    if len(Operator.objects.limit(1)) is not 0 and skip_if_exists:
        print("Skipping due to skip_if_exists: True")
        return

    result = DataSetMap.objects.only(['operator_id']).distinct()
    for data_set_map in result:
        Operator.create(operator_id=data_set_map.operator_id)
