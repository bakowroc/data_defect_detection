from db.models.CassandraBaseModel import CassandraBaseModel


class RawDataModel(CassandraBaseModel):
    def __init__(self, cassandra_object):
        self.model = dict(
            Id=None,
            KpiName=None,
            Date=None,
            Value=0
        )

        CassandraBaseModel.__init__(self, cassandra_object)
