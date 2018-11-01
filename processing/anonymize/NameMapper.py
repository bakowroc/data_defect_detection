import csv
import unicodedata


class NameMapper:
    def __init__(self):
        self.acronym_map = {}


    def map_acronym(self, acronym):
        if acronym in self.acronym_map:
            return self.acronym_map[acronym]

        name = self.get_name_value()
        self.acronym_map[acronym] = name
        return name


    def get_name_value(self):
        with open('cities.csv', 'r', encoding='utf8') as f:
            reader = csv.reader(f)
            names = list(reader)

        reserved_names = list(self.acronym_map.values())

        for name in names:
            parsed_name = unicodedata.normalize('NFKD', name[0]).upper().replace(' ', '_').replace('\'', '')
            if parsed_name not in reserved_names:
                return parsed_name

        return None

