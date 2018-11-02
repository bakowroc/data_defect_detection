from string import Template

from cassandra.cluster import ResultSet


class ValueData:
    def __init__(self, operator_id = None, acronym = None, kpi_name = None, date = None, value = None, cassandra_row = None):
        if cassandra_row is None:
            self.operator_id = operator_id
            self.acronym = acronym
            self.kpi_name = kpi_name
            self.date = date
            self.value = value
        else:
            self.operator_id = cassandra_row.operator_id
            self.acronym = cassandra_row.acronym
            self.kpi_name = cassandra_row.kpi_name
            self.date = cassandra_row.date
            self.value = cassandra_row.value

        self.table_name = 'value_data'


    def insert(self):
        query = Template("""
        INSERT INTO $table (operator_id, acronym, kpi_name, date, value) 
        VALUES($operator_id, '$acronym', '$kpi_name', '$date', $value)
        """)

        return query.substitute(
            table = self.table_name,
            operator_id = self.operator_id,
            acronym = self.acronym,
            kpi_name = self.kpi_name,
            date = self.date,
            value = self.value
        )