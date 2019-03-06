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

            parsed_result = []
            result = DataPoint.objects.filter(operator_id=operator_id, acronym=acronym, kpi_name=kpi_name)

            for data_point in result:
                parsed_result.append({
                    'value': data_point.value,
                    'date': str(time_uuid.TimeUUID.convert(data_point.date).get_datetime()),
                    'timestamp': time_uuid.TimeUUID.convert(data_point.date).get_timestamp()
                })

            detector = OutlierDetector(dataset=parsed_result)
            labeled_result = detector.knn_mean_featured(n_clusters=150, feature='monthday', distance_ratio=3, method='sim')
            resp.body = json.dumps(labeled_result, ensure_ascii=False)
            resp.status = falcon.HTTP_200
        except ValueError as err:
            resp.body = json.dumps({'error': "{}".format(str(err))})
            resp.status = falcon.HTTP_400

