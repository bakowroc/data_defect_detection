import json
import falcon
import time_uuid

from db.models.DataPoint import DataPoint


class DatasetRoute(object):
    @staticmethod
    def on_get(req, resp):
        try:
            operator_id = req.params['operator_id']
            acronym = req.params['acronym']
            kpi_name = req.params['kpi_name']

            body = []
            result = DataPoint.objects.filter(operator_id=operator_id, acronym=acronym, kpi_name=kpi_name)

            for data_point in result:
                body.append({
                    'value': data_point.value,
                    'date': str(time_uuid.TimeUUID.convert(data_point.date).get_datetime()),
                    'timestamp': time_uuid.TimeUUID.convert(data_point.date).get_timestamp()
                })

            resp.body = json.dumps(body, ensure_ascii=False)
            resp.status = falcon.HTTP_200
        except KeyError as err:
            missing_field = str(err)
            resp.body = json.dumps({'error': "{} is required".format(missing_field)})
            resp.status = falcon.HTTP_400
