import json
import falcon
import time_uuid

from db.models.Operator import Operator


class OperatorRoute(object):
    @staticmethod
    def on_get(req, resp):
        result = Operator.objects.all()

        body = []
        for operator_row in result:
            body.append({
                'operator_id': operator_row.operator_id,
                'operator_name': "LOREM"
            })

        resp.body = json.dumps(body, ensure_ascii=False)
        resp.status = falcon.HTTP_200

