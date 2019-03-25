run:
	python3 run.py
build:
	./build.sh
train:
	./train_model.sh
test:
	mypy eco --ignore-missing-imports && python3 -m unittest discover
