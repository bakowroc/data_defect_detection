import datetime

import time_uuid

from db.models.DataPoint import DataPoint
from db.models.DataSetMap import DataSetMap
from db.models.Report import Report
from outlier_detector.OutlierDetector import OutlierDetector
from utils.date import create_uuid


def run_all():
    print("Calculating outliers for all defined algorithms")
    if len(DataSetMap.objects.limit(1)) is 0:
        raise ResourceWarning("collection data_set_map is empty")

    result = DataSetMap.objects.all().filter(has_enough=True).allow_filtering()
    print(len(result))
    features = ['day', 'weekday', 'monthday', 'timestamp']

    for data_set in result:
        for feature in features:
            operator_id = data_set.operator_id
            acronym = data_set.acronym
            kpi_name = data_set.kpi_name

            data_points = DataPoint.objects.filter(operator_id=operator_id, acronym=acronym, kpi_name=kpi_name)
            detector = OutlierDetector(dataset=parse_result(data_points), feature=feature)
            run_kmean_dist(data_set, detector, feature)
            run_kmean_sim(data_set, detector, feature)


def run_kmean_dist(data_set, detector, feature):
    method = "kmean_dist"
    clusters = [10, 20, 40, 60, 80]
    distance_ratios = [1.2, 1.3, 1.6, 2, 2.5]

    start_time = datetime.datetime.now()
    for cluster in clusters:
        for distance_ratio in distance_ratios:
            outliers = list(filter(lambda p: p['is_outlier'], detector.knn_mean_dist(cluster, distance_ratio)))
            params = "{}|{}|{}".format(feature, cluster, distance_ratio)

            save_report(data_set, method, len(outliers), params, start_time, datetime.datetime.now())


def run_kmean_sim(data_set, detector, feature):
    method = "kmean_sim"
    clusters = [10, 20, 40, 60, 80]
    similarities = [1, 2, 3, 4]

    start_time = datetime.datetime.now()
    for cluster in clusters:
        for similarity in similarities:
            outliers = list(filter(lambda p: p['is_outlier'], detector.knn_mean_sim(cluster, similarity)))
            params = "{}|{}|{}".format(feature, cluster, similarity)

            save_report(data_set, method, len(outliers), params, start_time, datetime.datetime.now())


def save_report(data_set, method, count_outliers, params, start_time, end_time):
    Report.create(
        operator_id=data_set.operator_id,
        acronym=data_set.acronym,
        kpi_name=data_set.kpi_name,
        method=method,
        count_outliers=count_outliers,
        params=params,
        start_time=create_uuid(start_time),
        end_time=create_uuid(end_time)
    )


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
