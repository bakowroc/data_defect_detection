import json

from cassandra.cqlengine.query import ModelQuerySet


class CassandraDataEncoder(json.JSONEncoder):
    def default(self, cassandra_object: ModelQuerySet):
        keys = []
        for v in cassandra_object.model.__dict__['_defined_columns'].items():
            keys.append(v[0])

        result = []
        for row in cassandra_object:
            parsed_row = {}
            for key in keys:
                parsed_row[key] = row[key]

            result.append(parsed_row)

        return result
