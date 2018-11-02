from string import Template
from cassandra.cqltypes import DateType

class OperatorToAcronym:
    def __init__(self, operator_id = None, acronym = None, cassandra_row = None):
        if cassandra_row is None:
            self.operator_id = operator_id
            self.acronym = acronym
        else:
            self.operator_id = cassandra_row.operator_id
            self.acronym = cassandra_row.acronym

        self.table_name = 'operator_to_acronym'


    def insert(self):
        query = Template("INSERT INTO $table (operator_id, acronym) VALUES($operator_id, '$acronym');")

        return query.substitute(
            table=self.table_name,
            operator_id=self.operator_id,
            acronym=self.acronym
        )
