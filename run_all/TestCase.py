import datetime

OPTIMAL_CONFIGURATION = {
    'feature': 'none',
    'clusters': 30,
    'distance_ratio': 4,
    'similarity': 5,
    'precision': 0.5,
    'tolerance': 0.5
}


class TestCase:
    def __init__(self, configuration):
        self.id = datetime.datetime.now().time()
        self._configuration = {**OPTIMAL_CONFIGURATION, **configuration}
        self._durations = None

        self._feature = self._configuration['feature']
        self._results = {}
        self._results['dist_c'] = {
            'clusters': self._configuration['clusters'],
            'distance_ratio': self._configuration['distance_ratio'],
            'results': 0
        }

        self._results['dist_f'] = {
            'clusters': self._configuration['clusters'],
            'results': 0
        }

        self._results['reg'] = {
            'tolerance': self._configuration['tolerance'],
            'results': 0
        }

        self._results['sim'] = {
            'clusters': self._configuration['clusters'],
            'similarity': self._configuration['similarity'],
            'results': 0
        }

        self._results['fusion'] = {
            'precision': self._configuration['precision'],
            'results': 0
        }

    def get_configuration(self):
        return self._configuration

    def append_results(self, result_dict):
        self._durations = result_dict['durations']
        outliers = {}
        for k, v in result_dict['data'].items():
            if v is None:
                outliers[k] = None
            else:
                outliers[k] = len(list(filter(lambda dp: dp['is_outlier'], v)))

        self._results['dist_c']['results'] = outliers['knn_dist_c_result']
        self._results['dist_f']['results'] = outliers['knn_dist_f_result']
        self._results['sim']['results'] = outliers['knn_sim_result']
        self._results['reg']['results'] = outliers['regression_line_result']
        self._results['fusion']['results'] = outliers['fusion_result']

    def get_results(self):
        return self._results

    def get_durations(self):
        return self._durations
