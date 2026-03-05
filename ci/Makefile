all: install build

publish:
	python3 pdm.py publish

build:
	python3 build.py

install:
	python3 pdm.py install

sync:
	python3 pdm.py sync

pre-commit: format typing

format:
	python3 pre-commit.py format

typing:
	python3 pre-commit.py typing
