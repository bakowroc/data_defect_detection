from cassandra.cqlengine.columns import *
from cassandra.cqlengine.models import Model


class Operator(Model):
    operator_id = Integer(primary_key=True)
    has_enough = Boolean()

    __keyspace__ = "data_det"
    __table_name__ = "operators"
