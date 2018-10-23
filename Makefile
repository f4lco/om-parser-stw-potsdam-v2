
RUN = pipenv run python -m stw_potsdam

dependencies:
	pipenv sync --dev

run:
	$(RUN)

debug:
	FLASK_ENV=development $(RUN)

test:
	pipenv run python -m pytest -v --cov stw_potsdam

test_debug:
	pipenv run python -m pytest -v --trace

coverage:
	pipenv run python -m coveralls

.PHONY: dependencies run debug test test_debug coverage
