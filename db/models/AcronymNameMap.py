from string import Template

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.cqltypes import DateType


class AcronymNameMap(Model):
    raw_acronym = columns.Text(primary_key=True)
    acronym = columns.Text(primary_key=True)

    __keyspace__ = "data_det"
    __table_name__ = "acronym_name_map"
