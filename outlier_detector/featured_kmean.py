from math import *
from datetime import datetime
from sklearn.cluster import KMeans
import numpy as np


def get_dataset_with_day_feature(dataset, method):
    dataset_with_day = dataset
    for index, data in enumerate(dataset_with_day):
        daytime_timestamp = datetime.fromtimestamp(data['timestamp'])
        if method is 'day':
            day = daytime_timestamp.day

        if method is 'monthday':
            day = "{}{}".format(daytime_timestamp.day, daytime_timestamp.month)

        if method is 'weekday':
            day = daytime_timestamp.weekday()

        dataset_with_day[index]['day'] = day

    return dataset_with_day


def featured_kmean(n_clusters, raw_dataset, feature='day', method='dist', similarity=1, distance_ratio=1.5):
    dataset_with_day = get_dataset_with_day_feature(raw_dataset, feature)
    dataset = np.array(list(map(lambda data: [data['timestamp'], data['day'], data['value']], dataset_with_day)))
    model = KMeans(n_clusters)
    clusterer = model.fit(dataset)
    labels = model.predict(dataset)
    centroids = clusterer.cluster_centers_

    if method is 'sim':
        return use_similarity_variant(raw_dataset, labels, centroids, similarity)

    if method is 'dist':
        return use_distance_variant(raw_dataset, labels, centroids, distance_ratio)


def use_distance_variant(dataset, labels, centroids, distance_ratio):
    labeled_result = dataset
    centroids_with_distance = {}
    sorted_centroids = sorted(centroids, key=lambda c: c[0])

    # create centroid array with calculated distances to neighbour centroids
    for index, centroid in enumerate(sorted_centroids):
        current_centroid = list(centroid)
        centroid_index = str(centroids.tolist().index(current_centroid))
        c_point = [current_centroid[0], current_centroid[2]]  # [timestamp, day, value] -> [timestamp, value]

        try:
            prev_centroid = sorted_centroids[index-1]
            p_point = [prev_centroid[0], prev_centroid[2]]  # [timestamp, day, value] -> [timestamp, value]
            cp_vector = [c_point[0] - p_point[0], c_point[1] - p_point[1]]
        except IndexError:
            cp_vector = [0, 0]

        try:
            next_centroid = sorted_centroids[index+1]
            n_point = [next_centroid[0], next_centroid[2]]  # [timestamp, day, value] -> [timestamp, value]
            cn_vector = [c_point[0] - n_point[0], c_point[1] - n_point[1]]
        except IndexError:
            cn_vector = [0, 0]

        cp_dist = sqrt(cp_vector[0]**2 + cp_vector[1]**2)
        cn_dist = sqrt(cn_vector[0]**2 + cn_vector[1]**2)

        scalar_multiply = (cp_vector[0] * cn_vector[0]) + (cp_vector[1] * cn_vector[1])
        angle = degrees(cos(scalar_multiply / cp_dist * cn_dist))
        calculated_angle = angle if angle >= 0 else angle + 180

        current_centroid.append(cp_dist)
        current_centroid.append(cn_dist)
        current_centroid.append(calculated_angle)

        centroids_with_distance[centroid_index] = current_centroid

    for index, label in enumerate(labels):
        centroid_for_data_point = centroids_with_distance[str(label)]
        prev_distance = centroid_for_data_point[3]
        next_distance = centroid_for_data_point[4]
        angle = centroid_for_data_point[5]
        if labeled_result[index]['value'] == 0:
            print(centroid_for_data_point)
        distances = [prev_distance, next_distance]
        min_distance = min(distances) if min(distances) != 0 else max(distances)
        ratio_condition = max(distances) / min_distance > distance_ratio
        labeled_result[index]['is_outlier'] = ratio_condition or bool(angle < 30)
        labeled_result[index]['centroid_value'] = 0

    labeled_result = []
    for centroid in centroids:
        print(centroid)
        labeled_result.append({
            'timestamp': list(centroid)[0],
            'value': list(centroid)[1],
            'is_outlier': False
        })

    return labeled_result


def use_similarity_variant(dataset, labels, centroids, similarity):
    labeled_result = dataset
    centroids_counter = {}

    for index, label in enumerate(labels):
        key = str(centroids[label][2])
        try:
            centroids_counter[key] = centroids_counter[key] + 1
        except KeyError:
            centroids_counter[key] = 1

    for index, label in enumerate(labels):
        key = str(centroids[label][2])
        labeled_result[index]['is_outlier'] = centroids_counter[key] <= similarity

    labeled_result = []
    for centroid in centroids:
        print(centroid)
        labeled_result.append({
            'timestamp': list(centroid)[0],
            'value': list(centroid)[1],
            'is_outlier': False
        })

    return labeled_result

