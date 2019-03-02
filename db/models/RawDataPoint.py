from cassandra.cqlengine.columns import *
from cassandra.cqlengine.models import Model

from utils.date import generate_days, generate_months


class RawDataPoint(Model):
    kpi_basename = Text(primary_key=True)
    date = DateTime(primary_key=True)
    cord_id = BigInt(primary_key=True)
    acronym = Text(primary_key=True)
    kpi_name = Text()
    kpi_version = Text()
    to_be_deleted = Boolean()
    value = Double()

    __keyspace__ = "data_det"
    __table_name__ = "raw_data_points"

    @staticmethod
    def run_per_each(func):
        for data_range in generate_months():
            min_time = data_range[0]
            max_time = data_range[1]

            for day in generate_days(min_time, max_time):
                result = RawDataPoint.objects.all().filter(date=day).allow_filtering()
                for raw_data_point in result:
                    func(raw_data_point)

