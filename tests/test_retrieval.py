# -*- encoding: utf-8 -*-

import os
import pytest

from stw_potsdam import feed
from stw_potsdam.config import read_canteen_config
from stw_potsdam.canteen_api import download_menu
from stw_potsdam.canteen_api import MenuParams

ENV_ENABLED = 'ENABLE_API_QUERY'

CANTEENS = read_canteen_config()


@pytest.fixture(params=CANTEENS.values(), ids=lambda canteen: canteen.name)
def canteen(request):
    return request.param


requires_online_api = pytest.mark.skipif(
    not bool(os.getenv(ENV_ENABLED)),
    reason='Querying the online API is disabled. Turn on by setting env variable %s.' % ENV_ENABLED
)


@requires_online_api
def test_retrieval(canteen):
    menu = download_menu(MenuParams(canteen_id=canteen.id, chash=canteen.chash))
    feed.render_meta(canteen, menu)
    feed.render_menu(canteen, menu)
