from cassandra.cqlengine.columns import *
from cassandra.cqlengine.models import Model


class RawKpiDefinition(Model):
    partition_key = Text(primary_key=True)
    id = Integer(primary_key=True)
    calculator_class = Text()
    decimal_places = Integer()
    formula = Text()
    highest_is_best = Boolean()
    is_active = Boolean()
    is_simple = Boolean()
    max = Double()
    min = Double()
    nekpi_aggr_by_period_cl_at = DateTime()
    nekpi_calc_at = DateTime()
    period_calculator_class = Text()
    plmnkpi_aggr_by_cord_at = DateTime()
    plmnkpi_aggr_by_cord_group_at = DateTime()
    plmnkpi_aggr_by_period_at = DateTime()
    plmnkpi_aggr_by_period_cl_at = DateTime()
    plmnkpi_aggr_by_region_at = DateTime()
    plmnkpi_calc_at = DateTime()
    priority = Integer()
    tags = Text()
    technology = Text()
    text = Text()
    thresholds = List(Double)
    unit = Text()
    use_thresholds = Boolean()

    __keyspace__ = "data_det"
    __table_name__ = "raw_kpi_definitions"
