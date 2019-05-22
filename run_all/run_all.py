import json
import os

import time_uuid

from db.models.DataPoint import DataPoint
from db.models.DataSetMap import DataSetMap
from outlier_detector.OutlierDetector import OutlierDetector
from run_all.TEST_CASES import TEST_CASES

TEST_DATASETS = [
    {
        'operator_id': 53,
        'acronym': 'MOGILA',
        'kpi_name': 'LTE_1079'
    }
]


def run_all():
    print("Calculating outliers for all defined algorithms")
    if len(DataSetMap.objects.limit(1)) is 0:
        raise ResourceWarning("collection data_set_map is empty")

    features = ['day', 'weekday', 'monthday', 'none']

    for dataset in TEST_DATASETS:
        for feature in features:
            operator_id = dataset['operator_id']
            acronym = dataset['acronym']
            kpi_name = dataset['kpi_name']

            data_points = DataPoint.objects.filter(operator_id=operator_id, acronym=acronym, kpi_name=kpi_name)
            detector = OutlierDetector(dataset=parse_result(data_points), feature=feature)

            for test in TEST_CASES:
                options = test['OPTIONS']
                result_dict = detector.fusion(options)
                write_test_result(test, result_dict, dataset, feature)


def write_test_result(test, result_dict, dataset, feature):
    json_data = test
    json_data['OPTIONS']['feature'] = feature
    operator_id = dataset['operator_id']
    acronym = dataset['acronym']
    kpi_name = dataset['kpi_name']

    json_data['META'] = {
        'operator_id': operator_id,
        'acronym': acronym,
        'kpi_name': kpi_name,
    }

    json_data['RESULTS'] = {}
    for k, v in result_dict.items():
        outliers = list(map(lambda dp: [dp['value'], dp['timestamp']] if dp['is_outlier'] else None, v))
        json_data['RESULTS'][k] = list(filter(lambda o: o is not None, outliers))

    dir_name = './tests_results/{}-{}-{}'.format(operator_id, acronym, kpi_name)
    print(dir_name)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    file_name = '{}/{}-{}.json'.format(dir_name, feature, test['ID'])
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
