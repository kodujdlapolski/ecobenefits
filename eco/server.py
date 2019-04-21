from typing import Callable

import cerberus
from sanic import Sanic
from sanic.response import json

from eco import config
from eco.data_utils import load_models
from eco.eco_model import predict_all_benefits
from eco.utils import get_async_redis_conn
from eco.stats import EcoStatistics

app = Sanic()

schema = {'trunk_diam': {'type': 'float'}}


@app.listener('before_server_start')
async def setup(app, loop):
    app.models = load_models(config.MODELS_PATH)
    app.redis_conn = await get_async_redis_conn()


@app.listener('before_server_stop')
async def close_redis_conn(app, loop):
    app.redis_conn.close()


def validate(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        request = args[0]
        validator = cerberus.Validator(schema)
        try:
            validator.validate(request.json, schema)
        except cerberus.validator.DocumentError as e:
            return json({'description': e}, status=400)

        if validator.errors:
            return json(validator.errors, status=400)
        return func(*args, **kwargs)

    return wrapper


@app.route('/tree-benefits', methods=['POST', ])
@validate
def tree_benefits(request):
    benefits = predict_all_benefits(app.models, request.json['trunk_diam'])
    return json(benefits, status=200)


@app.route('/total-benefits', methods=['GET', ])
async def total_benefits(request):
    stats = EcoStatistics(app.redis_conn)
    total_stats = await stats.get_eco_stats()
    return json(total_stats, status=200)
