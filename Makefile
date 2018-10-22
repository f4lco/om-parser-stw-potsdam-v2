
RUN = pipenv run python -m stw_potsdam

dependencies:
	pipenv sync

run:
	$(RUN)

debug:
	FLASK_ENV=development $(RUN)

test:
	pipenv run python -m pytest -v

test_debug:
	pipenv run python -m pytest -v --trace

.PHONY: run debug test test_debug
