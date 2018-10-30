class CassandraBaseModel:
    def __init__(self, cassandra_object):
        self.cassandra_object = cassandra_object;
        self.model = {}

    def parse_model(self):
        for prop in self.cassandra_object:
            self.model[prop] = self.cassandra_object[prop]
