[![Build Status](https://travis-ci.com/sireliah/ecobenefits.svg?branch=master)](https://travis-ci.com/sireliah/ecobenefits)

# Ecobenefits
Every tree helps to aggregate polution by collecting it through leaves stomata. This service delivers estimated ecological benefits for trees in mapadrzew.pl. We are able to tell how many grams of pollution given tree is able to remove through a year. In particular we estimate amount of:

- O3
- SO2
- NO2
- PM2.5

Our simplified model is able to generalize data from around 6000 trees from Ogród Krasińskich in Warsaw and provide estimations based on tree trunk diameter.

The model is defined in this notebook: [Eco model](https://github.com/kodujdlapolski/tree-research/blob/master/model.ipynb) and based on the research:

[Z. Szkop, An evaluation of the ecosystem services provided by urban trees](https://www.researchgate.net/publication/312417053_An_evaluation_of_the_ecosystem_services_provided_by_urban_trees_The_role_of_Krasinski_Gardens_in_air_quality_and_human_health_in_Warsaw_Poland)

## How to start
To start the project, first create the virtualenv and install dependencies (service is designed to work with Python >= 3.7) using following command:
```
cd ecobenefits/

make build

source .venv/bin/activate
```
## How to test
This will run mypy type checks and unit tests.
```
make test
```
## How to train the model
For this service to work, we have to train the model on prepared data first. Since we cannot disclose this data in public repository, please contact us through [Koduj dla Polski](https://kodujdlapolski.pl/kontakt/) to get the training data.

```
cp training_trees.csv data/

make train
```
This will generate pickled models in `saved_models/` dir: `NO2.pkl`, `O3.pkl`, `PM2.5.pkl` and `SO2.pkl`. Now we're ready to run!

## How to run
This will start the Sanic http server.
```
make run

[19826] [INFO] Goin' Fast @ http://0.0.0.0:8888
[19826] [INFO] Starting worker [19826]
```

### Tree-benefits endpoint
The eco model is based on the tree trunk diameter, so we need to send the diameter through the request to see what benefis tree of given size provides.
```
http POST :8888/tree-benefits trunk_diam:=57.000000

HTTP/1.1 200 OK
Content-Type: application/json

{
    "NO2": 50.6408962856,
    "O3": 86.8929782983,
    "PM2.5": 4.6798194028,
    "SO2": 6.0842316844
}
```
Returned values are in **grams per year** units.

### Summary endpoint
Summary returns benefits for all trees that are present in the otm-core database.

The `make stats` command imports all trees and calculates benefits for them.

Results can be viewed as follows.
```
http :8888/summary

HTTP/1.1 200 OK
Content-Type: application/json

{
    "benefits": {
        "NO2": 50.6408962856,
        "O3": 86.8929782983,
        "PM2.5": 4.6798194028,
        "SO2": 6.0842316844
    },
    "trees_count": 1
}
```

Note: `http` command is provided by [httpie](https://httpie.org/).

