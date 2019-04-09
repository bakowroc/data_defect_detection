from db.models.DataPoint import DataPoint
from db.models.Operator import Operator


def load_operators(skip_if_exists=True):
    print("Loading operators")
    if len(DataPoint.objects.limit(1)) is 0:
        raise ResourceWarning("collection data_points is empty")

    if len(Operator.objects.limit(1)) is not 0 and skip_if_exists:
        print("Skipping due to skip_if_exists: True")
        return

    result = DataPoint.objects.only(['operator_id']).distinct()
    for data_point in result:
        Operator.create(operator_id=data_point.operator_id)
