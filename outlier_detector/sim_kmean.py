import numpy as np
from sklearn.cluster import KMeans


def sim_kmean(n_clusters, dataset, similarity):
    filtered_dataset = np.array(list(map(lambda data: [data['value'], data['day']], dataset)))
    model = KMeans(n_clusters)
    clusterer = model.fit(filtered_dataset)
    labels = model.predict(filtered_dataset)
    centroids = clusterer.cluster_centers_

    labeled_result = dataset
    centroids_counter = {}

    for index, label in enumerate(labels):
        key = str(centroids[label][0])
        try:
            centroids_counter[key] = centroids_counter[key] + 1
        except KeyError:
            centroids_counter[key] = 1

    for index, label in enumerate(labels):
        key = str(centroids[label][0])
        labeled_result[index]['is_outlier'] = centroids_counter[key] <= similarity
        labeled_result[index]['label'] = int(label)

    return labeled_result
