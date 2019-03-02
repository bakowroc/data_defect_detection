import json
import falcon

from db.models.DataSetMap import DataSetMap


class DatasetKeyRoute(object):
    @staticmethod
    def on_get(req, resp):
        try:
            operator_id = req.params['operator_id']
            result = DataSetMap.objects.filter(operator_id=operator_id)
            body = []
            for data_set_map in result:
                body.append({
                    'operator_id': data_set_map.operator_id,
                    'acronym': data_set_map.acronym,
                    'kpi_name': data_set_map.kpi_name
                })

            resp.body = json.dumps(body, ensure_ascii=False)
            resp.status = falcon.HTTP_200
        except KeyError as err:
            missing_field = str(err)
            resp.body = json.dumps({'error': "{} is required".format(missing_field)})
            resp.status = falcon.HTTP_400
