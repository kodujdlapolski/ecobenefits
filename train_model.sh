#!/bin/bash

set -e

source .venv/bin/activate

python3 -m eco.eco_model 'eco.eco_model.train()'
