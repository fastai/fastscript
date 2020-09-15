.ONESHELL:
SHELL := /bin/bash

SRC = $(wildcard *.ipynb)

all: fastscript docs

fastscript: $(SRC)
	nbdev_build_lib
	touch fastscript

docs_serve: docs
	cd docs && bundle exec jekyll serve

docs: $(SRC)
	rsync -a docs_src/ docs
	nbdev_build_docs
	touch docs

test:
	nbdev_test_nbs

release: pypi
	fastrelease_conda_package --upload_user fastai
	nbdev_bump_version

pypi: dist
	twine upload --repository pypi dist/*

dist: clean
	python setup.py sdist bdist_wheel

clean:
	rm -rf dist

