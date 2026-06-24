.PHONY: check validate test

check: validate test

validate:
	python3 scripts/validate_repository.py

test:
	python3 tests/test_validate_repository.py
