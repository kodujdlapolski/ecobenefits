from unittest import TestCase

from eco import config
from eco.eco_model import predict_all_benefits
from eco.data_utils import load_models


class TestModel(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.models = load_models(config.PROJECT_DIR + '/tests/models/')

    def test_predict_all_benefits(self):
        result = predict_all_benefits(self.models, 70.0)
        self.assertEqual(
            result, {
                'NO2': 65.62154430598939,
                'O3': 112.57662944757291,
                'PM2.5': 6.070727820995233,
                'SO2': 7.838204629215619
            })
