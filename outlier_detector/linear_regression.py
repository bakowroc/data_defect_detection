from sklearn.linear_model import LinearRegression
import numpy as np

from outlier_detector.learn_utils import create_windows


def linear_regression(dataset, acceptance=0.5, window_len=22, slide_len=2):
    x = np.array(list(map(lambda p: p['day'], dataset))).reshape(-1, 1)
    y = np.array(list(map(lambda p: p['value'], dataset))).reshape(-1, 1)
    model = LinearRegression()
    regressor = model.fit(x, y)

    outliers_counter = {}
    labels = {}
    labeled_result = dataset
    segments = create_windows(dataset, window_len, slide_len)

    for segment_num, segment in enumerate(segments):
        x_segment = np.array(list(map(lambda p: p['day'], segment))).reshape(-1, 1)

        values = regressor.predict(x_segment)

        for index, data_point in enumerate(segment):
            labels[data_point['id']] = segment_num
            condition_value = abs(data_point['value'] / values[index][0])
            is_outlier = condition_value > (1 + acceptance) or condition_value < (1 - acceptance)
            if is_outlier:
                try:
                    outliers_counter[data_point['id']] = outliers_counter[data_point['id']] + 1
                except KeyError:
                    outliers_counter[data_point['id']] = 1

    for index, data_point in enumerate(labeled_result):
        try:
            is_outlier = outliers_counter[data_point['id']] > int(0.75 * window_len / 2)
        except KeyError:
            is_outlier = False

        labeled_result[index]['is_outlier'] = is_outlier
        labeled_result[index]['label'] = labels[data_point['id']]

    return labeled_result
