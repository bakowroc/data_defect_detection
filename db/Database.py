from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.cluster import Cluster
from db.models.RawKpiDefinition import RawKpiDefinition
from db.models.KpiDefinition import KpiDefinition
from db.models.RawDataPoint import RawDataPoint
from db.models.DataPoint import DataPoint
from db.models.DataSetMap import DataSetMap
from db.models.AcronymNameMap import AcronymNameMap
from db.models.Operator import Operator


class Database:
    def __init__(self, database_config):
        connection.setup(['127.0.0.1'], "cqlengine", protocol_version=3)
        self.sync()

        self.keyspace = database_config['keyspace']
        self.cluster = Cluster()

    @staticmethod
    def sync():
        sync_table(RawKpiDefinition)
        sync_table(KpiDefinition)
        sync_table(RawDataPoint)
        sync_table(DataPoint)
        sync_table(DataSetMap)
        sync_table(AcronymNameMap)
        sync_table(Operator)

    def query(self, query):
        session = self.cluster.connect()
        session.set_keyspace(self.keyspace)

        try:
            result = session.execute(query)
            error = None

            session.shutdown()
            return result, error
        except EnvironmentError:
            result = None
            error = "Query to cassandra DB failed"

            session.shutdown()
            return result, error

