class RawDataModel:
    def __init__(self):
        self.id = None
        self.kpi_name = None
        self.date = None
        self.value = None
        self.table_name = 'raw_data'

    def apply(self, cassandra_object):
        self.id = cassandra_object.id
        self.value = cassandra_object.value
