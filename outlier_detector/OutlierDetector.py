from datetime import datetime

from outlier_detector.dist_kmean import dist_kmean
from outlier_detector.isolation_forest import isl_forest
from outlier_detector.learn_utils import flatten, count_duplicates
from outlier_detector.linear_regression import linear_regression
from outlier_detector.random_split import random_split
from outlier_detector.sim_kmean import sim_kmean


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

            if feature == 'monthday':
                day = "{}{}".format(daytime_timestamp.day, daytime_timestamp.month)

            if feature == 'weekday':
                day = daytime_timestamp.weekday()

            if feature == 'none':
                day = dataset_with_day[index]['timestamp']

            dataset_with_day[index]['day'] = int(day)

        return dataset_with_day

    def knn_mean_sim(self, clusters=30, similarity=10):
        outlier_detect_method = lambda: sim_kmean(clusters, self.dataset_with_day, similarity)
        return self.run_calculations(outlier_detect_method)

    def knn_mean_dist(self, clusters=30, variant='fixed', distance_ratio=2):
        outlier_detect_method = lambda: dist_kmean(clusters, self.dataset_with_day, variant, distance_ratio)
        return self.run_calculations(outlier_detect_method)

    def regression_line(self):
        return linear_regression(self.dataset_with_day)

    def isolation_forest(self):
        outlier_detect_method = lambda: isl_forest(self.dataset_with_day)
        return self.run_calculations(outlier_detect_method)

    def rnd_split(self):
        return random_split(self.dataset_with_day)

    def fusion(self, options):
        clusters = options['clusters']
        distance_ratio = options['distance_ratio']
        similarity = options['similarity']
        precision = options['precision']

        knn_sim_result = self.knn_mean_sim(clusters, similarity)
        knn_dist_f_result = self.knn_mean_dist(clusters, variant='fixed')
        knn_dist_c_result = self.knn_mean_dist(clusters, variant='calculated', distance_ratio=distance_ratio)
        regression_line_result = self.regression_line()

        fusion_result = self.get_fusion_result(
            [knn_sim_result, knn_dist_f_result, knn_dist_c_result, regression_line_result],
            precision=precision)

        return {
            'knn_sim_result': knn_sim_result,
            'knn_dist_f_result': knn_dist_f_result,
            'knn_dist_c_result': knn_dist_c_result,
            'regression_line_result': regression_line_result,
            'fusion_result': fusion_result
        }

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

    @staticmethod
    def get_fusion_result(methods, precision):
        tolerancy = precision * len(methods)
        outliers = []

        for index, method_result in enumerate(methods):
            method_outliers = []
            for data_point in method_result:
                if data_point['is_outlier']:
                    method_outliers.append(data_point['id'])

            outliers.append(method_outliers)

        occurrences = dict(count_duplicates(flatten(outliers)))
        final_result = []
        for data_point in methods[0]:
            if data_point['id'] in occurrences:
                is_outlier = occurrences[data_point['id']] >= tolerancy
                data_point['is_outlier'] = is_outlier

            final_result.append(data_point)

        return final_result
