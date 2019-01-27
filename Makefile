
RUN = pipenv run python -m stw_potsdam

dependencies:
	pipenv sync --dev

run:
	$(RUN)

debug:
	FLASK_ENV=development $(RUN)

test:
	pipenv run python -m pytest -v --cov-branch --cov stw_potsdam --cov-report term --cov-report html

test_debug:
	pipenv run python -m pytest -v --trace

coverage_publish:
	pipenv run python -m coveralls

coverage_report:
	pipenv run python -m coverage report --fail-under 90

lint:
	pipenv run pycodestyle stw_potsdam tests
	pipenv run pydocstyle stw_potsdam tests

clean:
	pipenv run python -m coverage erase
	rm -rf .pytest_cache .cache

.PHONY: dependencies run debug test test_debug coverage_publish coverage_report lint clean
