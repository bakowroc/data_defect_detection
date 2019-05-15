from random import randrange

import numpy as np


def random_split(dataset, splits_number=1):
    filtered_dataset = np.array(list(map(lambda data: [data['value'], data['timestamp']], dataset)))

    _min_v, _max_v = get_min_max(list(map(lambda dp: dp[0], filtered_dataset)))
    labeled_result = []
    chunks = []
    for split in range(0, splits_number):
        above = []
        below = []
        a = randrange(-10, 10) / randrange(0, 20)
        b = randrange(int(_min_v), int(_max_v))

        line = generate_line(a, b)

        for index, data_point in enumerate(filtered_dataset):
            x = data_point[1]
            y = data_point[0]

            if y < line(x):
                below.append(data_point)
                label = -1
            else:
                above.append(data_point)
                label = 1

            p = dataset[index]
            p['label'] = label
            p['is_outlier'] = False
            labeled_result.append(p)

        chunks.append(above)
        chunks.append(below)

    return labeled_result


def get_min_max(values):
    _min = np.min(values)
    _max = np.max(values)

    return _min, _max


def generate_line(a, b):
    print(a, b)

    def y(x):
        return a * -1 * (x / -1e9) + b

    return y
