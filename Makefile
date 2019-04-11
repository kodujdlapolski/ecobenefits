run:
	python3 run.py
build:
	./build.sh
train:
	python3 train.py
test:
	mypy eco --ignore-missing-imports && python3 -m unittest discover
