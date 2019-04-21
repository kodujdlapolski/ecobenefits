run:
	python run.py
build:
	./build.sh
train:
	python train.py
stats:
	python compute_stats.py
test:
	mypy eco --ignore-missing-imports && python -m unittest discover
