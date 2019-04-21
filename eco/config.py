import os

HOST = '0.0.0.0'
PORT = 8888

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 5

DB_USER = ''
DB_PASS = ''
DB_NAME = ''
DB_HOST = 'localhost'


FACTORS = [
    'O3',
    'NO2',
    'SO2',
    'PM2.5',
]

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

MODELS_PATH = os.path.join(PROJECT_DIR, 'saved_models/')
DATA_PATH = os.path.join(PROJECT_DIR, 'data/*.csv')
TRAINING_DATA_PATH = os.path.join('data/training_trees.csv')
