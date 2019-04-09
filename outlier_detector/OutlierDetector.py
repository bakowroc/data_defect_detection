from datetime import datetime

from outlier_detector.dist_kmean import dist_kmean
from outlier_detector.linear_regression import linear_regression
from outlier_detector.sim_kmean import sim_kmean
import numpy as np


class OutlierDetector:
    def __init__(self, dataset, feature):
        self.dataset = dataset
        self.dataset_with_day = self.get_dataset_with_day_feature(feature)

    def get_dataset_with_day_feature(self, feature):
        dataset_with_day = self.dataset
        for index, data in enumerate(dataset_with_day):
            daytime_timestamp = datetime.fromtimestamp(data['timestamp'])
            if feature == 'day':
                day = daytime_timestamp.day
                dataset_with_day[index]['timestamp'] = data['timestamp']

            if feature == 'monthday':
                day = "{}{}".format(daytime_timestamp.day, daytime_timestamp.month)
                dataset_with_day[index]['timestamp'] = data['timestamp']

            if feature == 'weekday':
                day = daytime_timestamp.weekday()
                dataset_with_day[index]['timestamp'] = data['timestamp']

            if feature == 'timestamp':
                day = data['timestamp']

            dataset_with_day[index]['day'] = int(day)

        return dataset_with_day

    def knn_mean_sim(self, clusters=30, similarity=2):
        outlier_detect_method = lambda: sim_kmean(clusters, self.dataset_with_day, similarity)
        return self.run_calculations(outlier_detect_method)

    def knn_mean_dist(self, clusters=30, distance_ratio=5):
        outlier_detect_method = lambda: dist_kmean(clusters, self.dataset_with_day, distance_ratio)
        return self.run_calculations(outlier_detect_method)

    def regression_line(self):
        return linear_regression(self.dataset_with_day)

    @staticmethod
    def run_calculations(method):
        iterations = 10
        labeled_result = []
        outliers_prob = {}

        for iteration in range(0, iterations):
            labeled_result = method()

            point_with_outliers = list(filter(lambda p: p['is_outlier'], labeled_result))
            for point in point_with_outliers:
                try:
                    outliers_prob[point['id']] = outliers_prob[point['id']] + 1
                except KeyError:
                    outliers_prob[point['id']] = 1

        final_result = []
        for data_point in labeled_result:
            try:
                is_outlier = outliers_prob[data_point['id']] / iterations > 0.5
            except KeyError:
                is_outlier = False

            final_result.append({
                'id': data_point['id'],
                'value': data_point['value'],
                'timestamp': data_point['timestamp'],
                'day': data_point['day'],
                'is_outlier': is_outlier,
                'label': data_point['label']
            })

        return final_result
