import json
import falcon

from db.models.KpiDefinition import KpiDefinition


class KpiDefinitionRoute(object):
    @staticmethod
    def on_get(req, resp):
        try:
            kpi_name = req.params['kpi_name']
            result = KpiDefinition.objects.all()
            filtered_result = list(filter(lambda kpi: kpi_name in kpi.formula, result))

            if len(filtered_result) is not 1:
                resp.body = json.dumps({'error': "found multiple or none matches"}, ensure_ascii=False)
                resp.status = falcon.HTTP_200
                return

            kpi_definition = filtered_result[0]
            body = {
                'id': kpi_definition.id,
                'description': kpi_definition.description,
                'formula': kpi_definition.formula,
                'tags': kpi_definition.tags,
                'technology': kpi_definition.technology,
                'unit': kpi_definition.unit
            }

            resp.body = json.dumps(body, ensure_ascii=False)
            resp.status = falcon.HTTP_200
        except KeyError as err:
            missing_field = str(err)
            resp.body = json.dumps({'error': "{} is required".format(missing_field)})
            resp.status = falcon.HTTP_400


