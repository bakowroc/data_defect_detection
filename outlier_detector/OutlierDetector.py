from outlier_detector.featured_kmean import featured_kmean
from outlier_detector.sliding_window_kmean import sliding_window_kmean
import numpy as np


class OutlierDetector:
    def __init__(self, dataset):
        self.dataset = dataset

    def knn_mean_featured(self, n_clusters, feature='day', method='dist', similarity=1, distance_ratio=1.5):
        return featured_kmean(n_clusters, self.dataset, feature, method, similarity, distance_ratio)

    def knn_mean_sliding(self, n_clusters):
        dataset = np.array(list(map(lambda data: data['value'], self.dataset)))
        return sliding_window_kmean(dataset, n_clusters)
