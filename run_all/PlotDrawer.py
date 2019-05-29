import glob
import csv
import math
import matplotlib.pyplot as plt
import numpy as np


class PlotDrawer:
    def __init__(self, chart_type, parameter):
        self._parameter = parameter
        self._type = chart_type
        self._reports = {}

    def draw(self):
        results = self.prepare_all_avg()
        keys = results['keys']

        fig, ax = plt.subplots()
        for method, outliers in results['data'].items():
            ax.plot(keys, outliers, marker='o')

        ax.set(ylabel='Number of outliers', xlabel=self._parameter,
               title='Result of changing {} parameter'.format(self._parameter))
        ax.grid()
        ax.legend(results['data'].keys())

        plt.savefig("./TESTS/{}_{}.png".format(self._type, self._parameter))

    def load_reports(self):
        reports = {
            'headers': [],
            'data': {}
        }

        files = glob.glob("./TESTS/*{}*.csv".format(self._parameter))
        for file in files:
            results = []
            dataset_key = '_'.join(file.split('_')[:4])

            with open(file, 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    results.append(row)

            reports['headers'] = results[0]
            reports['data'][dataset_key] = results[1:]

        self._reports = reports

    def prepare_all_avg(self):
        self.load_reports()
        data = self._reports['data']
        combined_values = {}

        for _, test_results in data.items():
            for test in test_results:
                y = test[1]
                x = test[2:]
                if y not in combined_values:
                    combined_values[y] = []

                combined_values[y].append(x)

        avg_results = {}
        for key, values in combined_values.items():
            avg_results[key] = [math.floor((sum(x) / len(values))) for x in zip(*PlotDrawer.to_ints(values))]

        return PlotDrawer.prepare_transposed_data(self._reports['headers'][2:], avg_results)

    @staticmethod
    def to_ints(values):
        int_values = values.copy()
        for index, value in enumerate(values):
            ints = list(map(int, value))
            int_values[index] = ints

        return int_values

    @staticmethod
    def prepare_transposed_data(headers, results):
        raw_data = []
        for k, v in results.items():
            raw_data.append(v)

        transposed_data = {
            'keys': list(results.keys()),
            'data': {}
        }

        transposed_values = np.array(raw_data).transpose()
        for index, row in enumerate(transposed_values):
            transposed_data['data'][headers[index]] = row

        return transposed_data
