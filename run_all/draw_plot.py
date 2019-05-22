import json
import glob

import numpy as np
import matplotlib.pyplot as plt

from run_all.run_all import TEST_DATASETS

INPUT_DIR = './tests_results'
features = ['day', 'weekday', 'monthday', 'none']
width = 0.1
ind = np.arange(-2, 3)


def draw_plot():
    for dataset in TEST_DATASETS:
        for feature in features:
            fig, ax = plt.subplots()
            create_bar_chart(ax, dataset, 'day')
            ax.set_xticks(ind)
            fig.tight_layout()
            plt.savefig("{}/{}.png".format(INPUT_DIR, feature))


def create_bar_chart(ax, dataset, feature):
    data = load_data_from_file(dataset)

    for index, result_tuple in enumerate(aggregate_by_feature(data)[feature].items()):
        ax.bar(ind + width * index, result_tuple[1], width, label=result_tuple[0])


def load_data_from_file(dataset):
    data = []
    dir_name = "{}/{}-{}-{}".format(INPUT_DIR, dataset['operator_id'], dataset['acronym'], dataset['kpi_name'])
    files = glob.glob(dir_name + '/*.json')

    for file in files:
        with open(file, 'r') as json_data:
            data.append(json.load(json_data))

    return data


def aggregate_by_feature(data):
    data_by_feature = {
        'day': {}, 'weekday': {}, 'monthday': {}, 'none': {}
    }

    for test_result in data:
        feature = test_result['OPTIONS']['feature']
        for method, result in test_result['RESULTS'].items():
            outliers = len(result)
            if method not in data_by_feature[feature]:
                data_by_feature[feature][method] = []

            data_by_feature[feature][method].append(outliers)

    return data_by_feature
