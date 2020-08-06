SRC = $(wildcard nbs/*.ipynb)

all: fastscript docs

fastscript: $(SRC)
	nbdev_build_lib
	touch fastscript

docs_serve: docs
	cd docs && bundle exec jekyll serve

docs: $(SRC)
	nbdev_build_docs
	touch docs

test:
	nbdev_test_nbs

release: pypi
	nbdev_conda_package
	cd conda
	conda build fastscript
	anaconda upload -u fastai ${CONDA_PREFIX}/conda-bld/noarch/*-py_0.tar.bz2
	rm ${CONDA_PREFIX}/conda-bld/noarch/*-py_0.tar.bz2
	cd ..
	nbdev_bump_version

pypi: dist
	twine upload --repository pypi dist/*

dist: clean
	python setup.py sdist bdist_wheel

clean:
	rm -rf dist

