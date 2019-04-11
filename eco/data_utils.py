import glob
import os
import pickle
from typing import Dict

import numpy as np
import pandas
from sklearn.linear_model import HuberRegressor

from eco import config
from eco.diameter_tools import get_trunk_diam


def load_data(files: str) -> pandas.DataFrame:
    data_files = glob.glob(files)

    datasets = []
    for _file in data_files:
        dataset = pandas.read_csv(_file)
        datasets.append(dataset)

    return pandas.concat(datasets)


def load_training_data(data_path: str) -> pandas.DataFrame:
    if not os.path.isfile(data_path):
        raise Exception(f'No training file in {data_path}')
    return pandas.read_csv(data_path, sep=';')


def prepare_data(data: pandas.DataFrame) -> pandas.DataFrame:
    data['norm'] = data['Obwód pnia w cm'].fillna('0')
    data.dropna(subset=['Obwód pnia w cm', 'norm'], inplace=True)
    data['norm'] = data['norm'].apply(pandas.Series)

    data['normalized_trunk_diam'] = data['norm'].apply(get_trunk_diam)
    data = data[data['normalized_trunk_diam'] > 0]

    data['height'] = data['Wysokość w m'].fillna('0')
    data['height'] = data['height'].str.replace(',', '.')
    data['height'] = data['height'].astype(np.float)
    return data


def prepare_training_data(tr_trees: pandas.DataFrame) -> pandas.DataFrame:
    tr_trees.dropna(inplace=True)
    tr_trees = tr_trees[tr_trees['OBWOD'] < 300]
    tr_trees = tr_trees[tr_trees['SREDNICA_KORONY'] < 20]
    tr_trees['KORONA_NORM'] = tr_trees['SREDNICA_KORONY'] * 100
    tr_trees['OBWOD_KW'] = tr_trees['OBWOD'] ** 2
    tr_trees['OBWOD_SQ'] = np.sqrt(tr_trees['OBWOD'])
    tr_trees['OBWOD_LOG'] = np.sqrt(tr_trees['OBWOD'])
    return tr_trees


def dump_models(models: Dict) -> None:
    for factor, model in models.items():
        with open(os.path.join(config.MODELS_PATH, f'{factor}.pkl'), 'wb') as desc:
            pickle.dump(model, desc)


def load_models(models_path: str) -> Dict[str, HuberRegressor]:
    models = {}
    model_files = {
        a: os.path.join(models_path, a + '.pkl') for a in config.FACTORS
    }

    assert model_files, f'Expected to find models in {models_path}'
    for factor, path in model_files.items():
        with open(path, 'rb') as desc:
            models[factor] = pickle.load(desc)

    return models
