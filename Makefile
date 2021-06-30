all: black flake8 isort mypy

black:
	black . \
		--exclude="(akad\/*|cherline\/*|line\/*|thrift_0_13_0\/*)"

flake8:
	flake8 .

isort:
	isort .

mypy:
	mypy .

run:
	python main.py -e dev
