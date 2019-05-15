from sklearn.ensemble import IsolationForest
import numpy as np

from outlier_detector.learn_utils import create_points_with_labels


def isl_forest(dataset):
    rng = np.random.RandomState(42)
    filtered_dataset = np.array(list(map(lambda data: [data['value'], data['day'], data['timestamp']], dataset)))
    clf = IsolationForest(n_estimators=100, behaviour='new', max_samples=100,
                          random_state=rng, contamination=0.01)

    clf.fit(filtered_dataset)
    prediction = clf.predict(filtered_dataset)

    labeled_result = []
    for data_point in create_points_with_labels(dataset, list(prediction)):
        data_point['is_outlier'] = data_point['label'] == -1
        labeled_result.append(data_point)

    return labeled_result
