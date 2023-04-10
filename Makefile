PYTHON_VERSION ?= 3.8

dist: clean-dist venv
	. venv/bin/activate && \
	pip3 install --upgrade pip build twine && \
	python3 -m build .

setup: venv

venv:
	virtualenv venv --python=${PYTHON_VERSION}

venv/.setup: dev-requirements.txt requirements.txt venv
	. venv/bin/activate && \
	pip3 install --upgrade pip && \
	pip3 install \
	--requirement dev-requirements.txt \
	--requirement requirements.txt && \
	touch venv/.setup

.PHONY: test
test: venv/.setup
	@ . venv/bin/activate && PYTHONPATH=src/ pytest -vv -s tests/ src/ --doctest-modules --doctest-continue-on-failure
	@ . venv/bin/activate && flake8 src --exclude '#*,~*,.#*'
	@ . venv/bin/activate && black --check src tests

.PHONY: watch
watch: venv/.setup
	@ . venv/bin/activate && PYTHONPATH=src/ pytest -vv -s tests/ src/ --doctest-modules --doctest-continue-on-failure
	@ . venv/bin/activate && PYTHONPATH=src/ ptw . -vv -s --doctest-modules --doctest-continue-on-failure

.PHONY: clean
clean: clean-dist
	rm -rf venv

.PHONY: clean-dist
clean-dist:
	rm -rf build
	rm -rf src/vidimera.egg-info
	rm -rf dist
