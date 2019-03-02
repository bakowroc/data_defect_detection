from cassandra.cqlengine.columns import *
from cassandra.cqlengine.models import Model


class DataPoint(Model):
    operator_id = BigInt(primary_key=True)
    acronym = Text(primary_key=True)
    kpi_name = Text(primary_key=True)
    date = TimeUUID(primary_key=True)
    value = Double()

    __keyspace__ = "data_det"
    __table_name__ = "data_points"
