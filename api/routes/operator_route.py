import json
import falcon

from api.json import CassandraDataEncoder
from db.models.Operator import Operator


class OperatorRoute(object):
    @staticmethod
    def on_get(_, resp):
        result = Operator.objects.all()

        resp.body = json.dumps(result, ensure_ascii=False, cls=CassandraDataEncoder)
        resp.status = falcon.HTTP_200
