from cassandra.cqlengine.columns import *
from cassandra.cqlengine.models import Model


class KpiDefinition(Model):
    id = Integer(primary_key=True)
    description = Text()
    formula = Text()
    tags = Text()
    technology = Text()
    unit = Text()

    __keyspace__ = "data_det"
    __table_name__ = "kpi_definitions"
