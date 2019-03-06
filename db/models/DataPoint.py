from cassandra.cqlengine.columns import *
from cassandra.cqlengine.functions import *
from cassandra.cqlengine.models import Model

from db.models.Operator import Operator
from utils.date import generate_months, create_uuid, generate_days


class DataPoint(Model):
    operator_id = BigInt(primary_key=True)
    acronym = Text(primary_key=True)
    kpi_name = Text(primary_key=True)
    date = TimeUUID(primary_key=True)
    value = Double()

    __keyspace__ = "data_det"
    __table_name__ = "data_points"

    @staticmethod
    def run_per_each(func):
        operators = Operator.objects.all()
        for operator in operators:
            print("Checking for operator: {}".format(operator.operator_id))
            for data_range in generate_months():
                min_time = data_range[0]
                max_time = data_range[1]

                for day in generate_days(min_time, max_time):
                    result = DataPoint.objects.only(['operator_id', 'acronym', 'kpi_name', 'date']).filter(operator_id=operator.operator_id, date=create_uuid(day)).allow_filtering()
                    for data_point in result:
                        func(data_point)
