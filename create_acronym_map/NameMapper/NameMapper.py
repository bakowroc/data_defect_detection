import csv
import unicodedata


class NameMapper:
    def __init__(self):
        self.value_map = {}

    def map_value(self, value):
        if value in self.value_map:
            return self.value_map[value]

        name = self.get_name_value()
        self.value_map[value] = name

    def get_name_value(self):
        with open('./fixtures/cities.csv', 'r', encoding='utf8') as f:
            reader = csv.reader(f)
            names = list(reader)

        reserved_names = list(self.value_map.values())

        for name in names:
            parsed_name = NameMapper.strip_accents(name[0]).upper().replace(' ', '_').replace('\'', '')
            if parsed_name not in reserved_names:
                return parsed_name

        return None

    @staticmethod
    def strip_accents(text):
            norm_text = unicodedata.normalize('NFD', text)
            norm_text = norm_text.encode('ascii', 'ignore')
            norm_text = norm_text.decode("utf-8")
            return str(norm_text)
