class DataReparser:
    def __init__(self, mode):
        self.mode = mode

    @staticmethod
    def raw_data_map(raw_data):
        return {
            "operator_id": raw_data.cord_id,
            "kpi_name": raw_data.kpi_name,
            "date": raw_data.date,
            "value": raw_data.date
        }

    @staticmethod
    def kpi_definitions_map(kpi):
        return {
            "definition_id": kpi.definition_id,
            "description": kpi.description,
            "technology": kpi.technology,
            "formula": kpi.formula,
            "unit": kpi.unit
        }

