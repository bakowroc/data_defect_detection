import numpy as np
from sklearn.cluster import KMeans

from outlier_detector.learn_utils import to_clusters, create_points_with_labels


def sim_kmean(n_clusters, dataset, similarity):
    filtered_dataset = np.array(list(map(lambda data: [data['value'], data['day'], data['timestamp']], dataset)))
    model = KMeans(n_clusters)
    model.fit(filtered_dataset)
    labels = model.predict(filtered_dataset)

    dataset_with_labels = create_points_with_labels(dataset, labels)

    clusters, clusters_dict = to_clusters(dataset, labels)
    _mean, _max = calculate_clusters_info(clusters)

    labeled_result = dataset_with_labels
    for index, data_point in enumerate(dataset_with_labels):
        labeled_result[index]['is_outlier'] = calculate_outlier_prob(_mean, _max, clusters_dict, data_point['label'],
                                                                     similarity)

    return labeled_result


def calculate_outlier_prob(_mean, _max, dict_clusters, label, similarity) -> bool:
    num_in_cluster = len(dict_clusters[label])
    return num_in_cluster <= int(_mean / similarity)


def calculate_clusters_info(clusters) -> (int, int):
    points_counter = []
    for cluster in clusters:
        points_counter.append(len(cluster))

    _mean = int(np.mean(points_counter))
    _max = int(np.max(points_counter))

    return _mean, _max
