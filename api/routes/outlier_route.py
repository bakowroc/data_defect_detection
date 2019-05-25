import json
import falcon
import time_uuid

from db.models.DataPoint import DataPoint
from outlier_detector.OutlierDetector import OutlierDetector


class OutlierRoute(object):
    @staticmethod
    def on_get(req, resp):
        try:
            operator_id = req.params['operator_id']
            acronym = req.params['acronym']
            kpi_name = req.params['kpi_name']
            feature = req.params['feature']
            method = req.params['method']

            parsed_result = []
            result = DataPoint.objects.filter(operator_id=operator_id, acronym=acronym, kpi_name=kpi_name)

            for index, data_point in enumerate(result):
                parsed_result.append({
                    'id': index,
                    'value': data_point.value,
                    'date': str(time_uuid.TimeUUID.convert(data_point.date).get_datetime()),
                    'timestamp': time_uuid.TimeUUID.convert(data_point.date).get_timestamp()
                })

            detector = OutlierDetector(dataset=parsed_result, feature=feature)

            final_result = []
            if method == 'sim':
                final_result, _ = detector.knn_mean_sim(similarity=5)

            if method == 'dist_f':
                final_result, _ = detector.knn_mean_dist(variant='fixed')

            if method == 'dist_c':
                final_result, _ = detector.knn_mean_dist(variant='calculated', distance_ratio=4)

            if method == 'reg':
                final_result, _ = detector.regression_line(tolerance=0.5)

            if method == 'isolation_forest':
                final_result, _ = detector.isolation_forest()

            if method == 'random_split':
                final_result, _ = detector.rnd_split()

            if method == 'fusion':
                final_result = detector.fusion({
                    'clusters': 30,
                    'distance_ratio': 4,
                    'similarity': 5,
                    'precision': 0.5,
                    'tolerance': 0.5
                })['data']['fusion_result']

            resp.body = json.dumps(final_result, ensure_ascii=False)
            resp.status = falcon.HTTP_200
        except ValueError as err:
            resp.body = json.dumps({'error': "{}".format(str(err))})
            resp.status = falcon.HTTP_400
