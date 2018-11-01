SHELL=/bin/bash

PY_VENV=.venv
PY_CMD=${PY_VENV}/bin/python
PIP_CMD=${PY_VENV}/bin/pip

.PHONY: setup-dev
setup-dev: .venv ${PY_VENV}/requirements-common.timestamp ${PY_VENV}/requirements-dev.timestamp

.PHONY: setup-prod
setup-prod: .venv ${PY_VENV}/requirements-common.timestamp ${PY_VENV}/requirements-prod.timestamp

.PHONY: serve-dev
serve-dev: setup-dev
	${PY_CMD} app.py dev

.PHONY: serve-prod
serve-prod:
	${PY_CMD} app.py prod

.venv:
	python3.6 -m venv .venv
	${PIP_CMD} install --upgrade pip

${PY_VENV}/requirements-common.timestamp: requirements/common.txt
	${PIP_CMD} install -r $<
	touch $@

${PY_VENV}/requirements-dev.timestamp: requirements/dev.txt
	${PIP_CMD} install -r $<
	touch $@

${PY_VENV}/requirements-prod.timestamp: requirements/prod.txt
	${PIP_CMD} install -r $<
	touch $@

.PHONY: cleanall
cleanall:
	rm -rf .venv