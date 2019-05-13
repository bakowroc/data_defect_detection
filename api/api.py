from api.app import StandaloneApplication
from api.routes.dataset_key_route import DatasetKeyRoute
from api.routes.dataset_route import DatasetRoute

import falcon
import multiprocessing

from api.routes.kpi_definition_route import KpiDefinitionRoute
from api.routes.operator_route import OperatorRoute
from api.routes.outlier_route import OutlierRoute
from config.APPConfig import APPConfig
from db.Database import Database

# TODO
cfg = APPConfig()
Database(cfg.read("database"))

api = application = falcon.API()
api.add_route('/dataset_keys', DatasetKeyRoute())
api.add_route('/datasets', DatasetRoute())
api.add_route('/operators', OperatorRoute())
api.add_route('/kpi_definitions', KpiDefinitionRoute())
api.add_route('/outliers', OutlierRoute())


# TODO Database connection freezes when using code below via cli


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


def server():
    options = {
        'bind': '%s:%s' % ('127.0.0.1', '8080'),
        'workers': number_of_workers(),
        'reload': True,
        'timeout': 100000
    }

    api = application = falcon.API()
    api.add_route('/dataset_keys', DatasetKeyRoute())
    api.add_route('/datasets', DatasetRoute())
    api.add_route('/operators', OperatorRoute())

    StandaloneApplication(application, options).run()
