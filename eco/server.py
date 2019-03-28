from typing import Callable

import cerberus
from sanic import Sanic
from sanic.response import json

from eco.data_utils import load_models
from eco.eco_model import predict_all_benefits

app = Sanic()
models = load_models()

schema = {'trunk_diam': {'type': 'float'}}


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


@app.route('/benefits', methods=['POST', ])
@validate
async def root(request):
    benefits = await predict_all_benefits(models, request.json['trunk_diam'])
    return json(benefits, status=200)
