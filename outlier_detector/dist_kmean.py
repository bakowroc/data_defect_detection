import numpy as np
from sklearn.cluster import KMeans
from math import hypot

from outlier_detector.learn_utils import create_points_with_labels


def dist_kmean(n_clusters, dataset, variant, distance_ratio):
    filtered_dataset = np.array(list(map(lambda data: [data['value'], data['day'], data['timestamp']], dataset)))
    model = KMeans(n_clusters)
    clusterer = model.fit(filtered_dataset)
    labels = model.predict(filtered_dataset)
    centroids = clusterer.cluster_centers_
    dataset_with_labels = create_points_with_labels(dataset, labels)

    distances = calculate_distances(dataset_with_labels, centroids)
    max_values_with_ratio = calculate_ratio(dataset_with_labels, distances)

    # Calculate outliers based on given method
    labeled_result = dataset_with_labels
    for index, data_point in enumerate(dataset_with_labels):
        if data_point['id'] in [_id for _id in max_values_with_ratio.keys()]:
            if variant == 'fixed':
                is_outlier = get_fixed_outliers(data_point, max_values_with_ratio)
            elif variant == 'calculated':
                is_outlier = get_calculated_outliers(data_point, max_values_with_ratio, distance_ratio)
        else:
            is_outlier = False

        labeled_result[index]['is_outlier'] = is_outlier

    return labeled_result


def calculate_points_distance(centroid, data_point) -> float:
    _x = (centroid[0] - data_point['value']) ** 2
    _y = (centroid[1] - data_point['day']) ** 2
    _z = (centroid[2] - data_point['timestamp']) ** 2

    _sum = np.sum(_x + _y + _z)
    return np.sqrt(_sum)


def calculate_distances(dataset, centroids):
    distances = {}
    for data_point in dataset:
        label = data_point['label']
        if label not in distances:
            distances[label] = {}

        distances[label][data_point['id']] = calculate_points_distance(centroids[label], data_point)

    return distances


def calculate_ratio(dataset, distances):
    max_values_with_ratio = {}
    for data_point in dataset:
        _min, _max, _mean = get_cluster_info(distances[data_point['label']])
        dist = distances[data_point['label']][data_point['id']]
        is_max_point = dist == _max
        if is_max_point:
            max_values_with_ratio[data_point['id']] = dist / _min

    return max_values_with_ratio


def get_cluster_info(cluster_distances):
    values_arr = []
    for k, v in cluster_distances.items():
        values_arr.append(v)

    _min = np.min(values_arr)
    _max = np.max(values_arr)
    _mean = np.mean(values_arr)

    return _min, _max, _mean


def get_fixed_outliers(data_point, ratios):
    sorted_ratios = sorted(ratios.items(), key=lambda kv: kv[1])
    print(sorted_ratios[-5:])
    outliers = []
    for _tuple in sorted_ratios[-5:]:
        outliers.append(_tuple[0])

    print(outliers)
    return data_point['id'] in outliers


def get_calculated_outliers(data_point, ratios, distance_ratio):
    return True
