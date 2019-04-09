import json
import falcon

from db.models.Operator import Operator


class OperatorRoute(object):
    @staticmethod
    def on_get(req, resp):
        result = Operator.objects.all()

        body = []
        for operator_row in result:
            body.append({
                'operator_id': operator_row.operator_id,
                'operator_name': "OPERATOR",
                'has_enough': operator_row.has_enough,
            })

        resp.body = json.dumps(body, ensure_ascii=False)
        resp.status = falcon.HTTP_200

