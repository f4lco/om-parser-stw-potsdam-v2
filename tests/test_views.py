# -*- encoding: utf-8 -*-
import pytest

from stw_potsdam import views
from flask import url_for

from tests.response_util import meal_names

# pytest fixtures are linked via parameter names of test methods
# pragma pylint: disable=unused-import,redefined-outer-name,unused-argument
from tests.stub_api import api_offline, api_online_one_shot

# Long test method names are not 'snake case'!
# See https://github.com/PyCQA/pylint/issues/2047
# The fix has not been ported to Python 2.x.
# pylint: disable=invalid-name


def test_health_check(client):
    response = client.get("/health_check")
    assert response.status_code == 200
    assert response.data == b"OK"


def test_index(client):
    response = client.get("/").json
    canteen_url = response.get("griebnitzsee", None)
    assert canteen_url, "Known canteen in index response"

    canteen = client.get(canteen_url)
    assert canteen.status_code == 200, "Canteen URL is reachable"


@pytest.mark.parametrize(
    "url",
    [
        "/canteens/spam",
        "/canteens/spam/xml",
    ],
)
def test_canteen_not_found(client, url):
    response = client.get(url)
    assert response.status_code == 404
    assert b"Canteen 'spam' not found" in response.data


@pytest.mark.xfail(strict=True)
def test_canteen_menu_api_unavailable(client, api_offline):
    _request_check_meals(client)


@pytest.mark.xfail(strict=True)
def test_canteen_menu_request(client, api_online_one_shot):
    raise NotImplementedError()
    _request_check_meals(client)


@pytest.mark.xfail(strict=True)
def test_canteen_menu_cached(client, api_online_one_shot):
    raise NotImplementedError()
    _request_check_meals(client)
    _request_check_meals(client)


@pytest.mark.xfail(strict=True)
def test_canteen_menu_second_request_indeed_fails(client, api_online_one_shot):
    _request_check_meals(client)
    views.cache.clear()
    _request_check_meals(client)


@pytest.mark.xfail(strict=True)
def _request_check_meals(client):
    raise NotImplementedError()
    response = client.get("/canteens/griebnitzsee/xml")
    assert response.status_code == 200
    meal = meal_names(response.data)[0]
    print(meal)
    # assert meal == "Gefüllter Germknödel \nmit Vanillesauce und Mohnzucker"


@pytest.fixture
def client():
    views.app.config["TESTING"] = True
    return views.app.test_client()


@pytest.fixture(autouse=True)
def clear_cache():
    yield
    views.cache.clear()
