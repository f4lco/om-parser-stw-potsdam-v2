# -*- encoding: utf-8 -*-

import json
import logging
import os
import pytest
from stw_potsdam.config import read_canteen_config
from stw_potsdam.views import canteen_xml_feed, app

# pragma pylint: disable=invalid-name,redefined-outer-name

ENV_ENABLED = 'ENABLE_API_QUERY'

# Because log messages are automatically part of the Pytest report, below
# explicitly avoids adding log handlers via logging#basicConfig, for example.
logging.getLogger().setLevel(logging.DEBUG)

CANTEENS = read_canteen_config()


@pytest.fixture(params=CANTEENS.values(), ids=lambda canteen: canteen.name)
def canteen(request):
    return request.param


def is_enabled():
    return bool(os.getenv(ENV_ENABLED))


requires_online_api = pytest.mark.skipif(
    not is_enabled(),
    reason="Querying the online API is disabled. "
           f"Turn on by setting env variable {ENV_ENABLED}."
)


@requires_online_api
def test_retrieval(canteen):
    try:
        with app.app_context(), app.test_request_context():
            canteen_xml_feed(canteen.key)
    except json.JSONDecodeError as e:
        pytest.xfail('JSON endpoint returned garbage (issue #6)')
        raise e  # Appease PyCharm inspection - xfail always raises
