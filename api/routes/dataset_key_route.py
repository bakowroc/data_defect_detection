import json
import falcon

from api.json import CassandraDataEncoder
from db.models.DataSetMap import DataSetMap


class DatasetKeyRoute(object):
    @staticmethod
    def on_get(req, resp):
        try:
            operator_id = req.params['operator_id']
            result = DataSetMap.objects.filter(operator_id=operator_id)

            resp.body = json.dumps(result, ensure_ascii=False, cls=CassandraDataEncoder)
            resp.status = falcon.HTTP_200
        except KeyError as err:
            missing_field = str(err)
            resp.body = json.dumps({'error': "{} is required".format(missing_field)})
            resp.status = falcon.HTTP_400
