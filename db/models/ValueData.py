from string import Template


class ValueData:
    def __init__(self, operator_id, acronym, kpi_name, date, value):
        self.operator_id = operator_id
        self.acronym = acronym
        self.kpi_name = kpi_name
        self.date = date
        self.value = value

        self.table_name = 'value_data'


    def insert(self):
        query = Template("INSERT INTO $table (operator_id, acronym, kpi_name, date, value) VALUES($operator_id, '$acronym', '$kpi_name', '$date', $value)")

        return query.substitute(
            table = self.table_name,
            operator_id = self.operator_id,
            acronym = self.acronym,
            kpi_name = self.kpi_name,
            date = self.date,
            value = self.value
        )