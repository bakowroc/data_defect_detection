from string import Template

from cassandra.cluster import Cluster


class Database:
    def __init__(self, database_config):
        self.keyspace = database_config['keyspace']
        self.cluster = Cluster()
        self.session = self.cluster.connect()

        try:
            self.session.set_keyspace(self.keyspace)
        except Exception:
            print("Keyspace does not exist. Creatng new one.")
            self.initialize()


    def execute_query(self, query):
        try:
            result = self.session.execute(query)
            error = None

            return result, error
        except EnvironmentError:
            result = None
            error = "Query to cassandra DB failed"

            return result, error


    def get_all(self, table_name):
        query_template = Template("SELECT * FROM $table_name;")
        query = query_template.substitute(table_name=table_name)

        return self.execute_query(query)


    def get_by_fields(self, table_name, fields):
        query_template = Template("SELECT $fields FROM $table_name;")
        fields_string = ','.join(fields)
        query = query_template.substitute(fields=fields_string, table_name=table_name)

        return self.execute_query(query)


    def get_by_dates(self, table_name, dates):
        query_template = Template("SELECT * FROM $table_name WHERE date IN($dates);")
        dates_string = "'" + "','".join(dates) + "'"
        print(dates)
        print(dates_string)
        query = query_template.substitute(table_name=table_name, dates=dates_string)
        print(query)

        return self.execute_query(query)


    def initialize(self):
        self.session.execute("""
            CREATE KEYSPACE %s
            WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
            """ % self.keyspace)

        self.session.set_keyspace(self.keyspace)
