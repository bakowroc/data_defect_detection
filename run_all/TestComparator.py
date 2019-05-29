from run_all.PlotDrawer import PlotDrawer


class TestComparator:
    def __init__(self, parameter, cases, algorithms=['_all_']):
        self._parameter = parameter
        self._cases = cases
        self._algorithms = algorithms

        self._dataset = None

    def save_dataset(self, dataset):
        self._dataset = dataset

    def get_test_cases(self):
        return self._cases

    def get_algorithms(self):
        return self._algorithms

    def get_parameter(self):
        return self._parameter

    def generate_data_summary(self):
        results_key = []
        for key, value in self._cases[0].get_results().items():
            if value['results'] is not None:
                results_key.append(key)

        data = [
            ['test_id', self._parameter, *results_key]
        ]

        for test in self._cases:
            row_data = [test.id, test.get_configuration()[self._parameter]]
            for key, value in test.get_results().items():
                if value['results'] is not None:
                    row_data.append(value['results'])

            data.append(row_data)

        return data

    def generate_csv(self):
        filename = '{}_{}_{}_{}_{}.csv'.format(
            self._dataset[0],
            self._dataset[1],
            self._dataset[2],
            self._parameter,
            '_'.join(self._algorithms)
        )

        data = self.generate_data_summary()
        with open("./TESTS/" + filename, 'w+') as file:
            for row in data:
                file.write(','.join(str(e) for e in row) + '\n')
