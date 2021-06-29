all: black flake8 isort mypy

black:
	black .

flake8:
	flake8 .

isort:
	isort .

mypy:
	mypy .

run:
	python main.py
