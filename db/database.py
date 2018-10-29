from cassandra.cluster import Cluster


class database:
    def __init__(self, database_config):
        self.keyspace = database_config['keyspace']
        self.cluster = Cluster()
        self.session = self.cluster.connect()

        try:
            self.session.set_keyspace(self.keyspace)
        except:
            self.initialize()


    def execute_query(self, query):
        return self.session.execute(query)

    def initialize(self):
        self.session.execute("""
            CREATE KEYSPACE %s
            WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
            """ % self.keyspace)

        self.session.set_keyspace(self.keyspace)
