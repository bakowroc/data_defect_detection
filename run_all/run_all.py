import datetime
import json

import time_uuid

from db.models.DataPoint import DataPoint
from db.models.DataSetMap import DataSetMap
from db.models.Report import Report
from outlier_detector.OutlierDetector import OutlierDetector
from utils.date import create_uuid

TEST_CASES = [
    {
        'ID': 1,
        'OPTIONS': {
            'clusters': 30,
            'distance_ratio': 6,
            'similarity': 5,
            'precision': 0.5
        }
    }
]


def run_all():
    print("Calculating outliers for all defined algorithms")
    if len(DataSetMap.objects.limit(1)) is 0:
        raise ResourceWarning("collection data_set_map is empty")

    result = DataSetMap.objects.all().filter(has_enough=True).limit(5).allow_filtering()
    features = ['day', 'weekday', 'monthday', 'none']

    for dataset in result:
        for feature in features:
            operator_id = dataset.operator_id
            acronym = dataset.acronym
            kpi_name = dataset.kpi_name

            data_points = DataPoint.objects.filter(operator_id=operator_id, acronym=acronym, kpi_name=kpi_name)
            detector = OutlierDetector(dataset=parse_result(data_points), feature=feature)
            for test in TEST_CASES:
                options = test['OPTIONS']
                result_dict = detector.fusion(options)
                write_test_result(test, result_dict, dataset)


def write_test_result(test, result_dict, dataset):
    json_data = test
    operator_id = dataset.operator_id
    acronym = dataset.acronym
    kpi_name = dataset.kpi_name

    json_data['META'] = {
        'operator_id': operator_id,
        'acronym': acronym,
        'kpi_name': kpi_name,
    }

    json_data['RESULTS'] = {}
    for k, v in result_dict.items():
        outliers = list(map(lambda dp: [dp['value'], dp['timestamp']] if dp['is_outlier'] else None, v))
        json_data['RESULTS'][k] = list(filter(lambda o: o is not None, outliers))

    file_name = './tests_results/{}-{}-{}-{}.json'.format(test['ID'], operator_id, acronym, kpi_name)
    with open(file_name, 'w+') as outfile:
        json.dump(json_data, outfile)


def parse_result(data_set):
    parsed_result = []
    for index, data_point in enumerate(data_set):
        parsed_result.append({
            'id': index,
            'value': data_point.value,
            'date': str(time_uuid.TimeUUID.convert(data_point.date).get_datetime()),
            'timestamp': time_uuid.TimeUUID.convert(data_point.date).get_timestamp()
        })

    return parsed_result
