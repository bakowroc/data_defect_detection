from cassandra.cqlengine.columns import *
from cassandra.cqlengine.models import Model


class Report(Model):
    operator_id = BigInt(primary_key=True)
    acronym = Text(primary_key=True)
    kpi_name = Text(primary_key=True)
    start_time = TimeUUID(primary_key=True)
    method = Text()
    params = Text()
    count_outliers = BigInt()
    end_time = TimeUUID()

    __keyspace__ = "data_det"
    __table_name__ = "reports"
