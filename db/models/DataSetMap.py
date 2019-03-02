from string import Template

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.cqltypes import DateType


class DataSetMap(Model):
    operator_id = columns.BigInt(primary_key=True)
    acronym = columns.Text(primary_key=True)
    kpi_name = columns.Text(primary_key=True)

    __keyspace__ = "data_det"
    __table_name__ = "data_set_map"
