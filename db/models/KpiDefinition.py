from string import Template
from cassandra.cqltypes import DateType


class KpiDefinition:
    def __init__(self, definition_id = None, formula = None, date = None, tags = None, technology = None, unit = None, cassandra_row = None):
        if cassandra_row is None:
            self.definition_id = definition_id
            self.formula = formula
            self.date = date
            self.tags = tags
            self.technology = technology
            self.unit = unit
        else:
            self.definition_id = cassandra_row.definition_id
            self.formula = cassandra_row.formula
            self.date = cassandra_row.date
            self.tags = cassandra_row.tags
            self.technology = cassandra_row.technology
            self.unit = cassandra_row.unit

        self.table_name = 'kpi_definitions'


    def insert(self):
        query = Template("""
        INSERT INTO $table (definition_id, formula, date, tags, technology, unit) 
        VALUES($definition_id, '$formula', '$date', '$tags', '$technology', '$unit');
        """)

        return query.substitute(
            table=self.table_name,
            definition_id=int(self.definition_id),
            formula=self.formula,
            date=str(self.date)[:-3],
            tags=self.tags,
            technology=self.technology,
            unit=self.unit
        )
