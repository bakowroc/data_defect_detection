import numpy as np
from sklearn.cluster import KMeans
from math import hypot


def dist_kmean(n_clusters, dataset, distance_ratio):
    filtered_dataset = np.array(list(map(lambda data: [data['value'], data['day']], dataset)))
    model = KMeans(n_clusters)
    clusterer = model.fit(filtered_dataset)
    labels = model.predict(filtered_dataset)
    centroids = clusterer.cluster_centers_

    distances = {}
    labeled_result = dataset

    for index, data_point in enumerate(dataset):
        self_centroid = centroids[labels[index]]
        dist = hypot(self_centroid[0] - data_point['value'], self_centroid[1] - data_point['day'])
        distances[index] = dist

    distances_in_tuples = sorted(distances.items(), key=lambda kv: kv[1])
    mid_val = distances_in_tuples[int(len(dataset) / 2)]

    outlier_ids = []
    # for dist in distances_in_tuples:
    #     if dist[1] > mid_val[1] * distance_ratio:
    #         outlier_ids.append(dist[0])

    for dist in distances_in_tuples[-5:]:
        outlier_ids.append(dist[0])

    for index, data_point in enumerate(labeled_result):
        labeled_result[index]['is_outlier'] = index in outlier_ids
        labeled_result[index]['label'] = int(labels[index])

    return labeled_result
