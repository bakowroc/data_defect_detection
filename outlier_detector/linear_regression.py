from sklearn.linear_model import LinearRegression
import numpy as np


def linear_regression(dataset):
    x = []
    y = []
    for data_point in dataset:
        x.append(data_point['day'])
        y.append(data_point['value'])

    x = np.array(x).reshape(-1, 1)
    y = np.array(y).reshape(-1, 1)

    model = LinearRegression()
    regressor = model.fit(x, y)
    values = regressor.predict(x)

    distances = {}
    labeled_result = dataset
    outlier_ids = []

    for index, data_point in enumerate(dataset):
        dist = abs(values[index][0] - data_point['value'])
        distances[index] = dist

    distances_in_tuples = sorted(distances.items(), key=lambda kv: kv[1])
    mid_val = distances_in_tuples[int(len(dataset) / 2)]

    for dist in distances_in_tuples[-5:]:
        outlier_ids.append(dist[0])

    for index, data_point in enumerate(labeled_result):
        labeled_result[index]['is_outlier'] = index in outlier_ids
        labeled_result[index]['label'] = 0

    return labeled_result
