PYTHON ?= python3
VENV ?= .venv
VENV_PYTHON := $(VENV)/bin/python
VENV_PIP := $(VENV)/bin/pip

.PHONY: check setup validate generate examples test bundle clean

check: setup generate validate examples test bundle

setup:
	$(PYTHON) -m venv $(VENV)
	$(VENV_PIP) install -q -r requirements.txt

generate:
	$(VENV_PYTHON) scripts/generate_artifacts.py

validate:
	$(VENV_PYTHON) scripts/validate_repository.py

examples:
	$(VENV_PYTHON) scripts/validate_examples.py

test:
	$(VENV_PYTHON) tests/test_validate_repository.py

bundle:
	$(VENV_PYTHON) scripts/build_release_bundle.py

clean:
	rm -rf $(VENV) dist/vault-schema-v*.zip dist/checksums.txt
