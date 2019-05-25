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

    def generate_data_summary(self):
        results_key = []
        durations = []
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
                    durations.append(round(test.get_durations()[key], 2))

            data.append(row_data)

        data.insert(0,  ['-', '-', *durations[:len(results_key)]])
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

    def draw_plot(self):
        pass
