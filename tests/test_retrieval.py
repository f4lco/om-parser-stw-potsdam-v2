# -*- encoding: utf-8 -*-

import os
import pytest

from stw_potsdam import feed
from stw_potsdam.config import read_canteen_config
from stw_potsdam.canteen_api import download_menu
from stw_potsdam.canteen_api import MenuParams

# pragma pylint: disable=invalid-name,redefined-outer-name

ENV_ENABLED = 'ENABLE_API_QUERY'

CANTEENS = read_canteen_config()


@pytest.fixture(params=CANTEENS.values(), ids=lambda canteen: canteen.name)
def canteen(request):
    return request.param


def is_enabled():
    user_enabled = bool(os.getenv(ENV_ENABLED))
    travis_enabled = os.getenv('TRAVIS_EVENT_TYPE') == 'cron'
    return user_enabled or travis_enabled


requires_online_api = pytest.mark.skipif(
    not is_enabled(),
    reason='Querying the online API is disabled. '
           'Turn on by setting env variable %s.' % ENV_ENABLED
)


@requires_online_api
def test_retrieval(canteen):
    feed.render_meta(canteen, "/canteens/{}/menu".format(canteen.key))
    params = MenuParams(canteen_id=canteen.id, chash=canteen.chash)
    menu = download_menu(params)
    feed.render_menu(menu)
