# -*- encoding: utf-8 -*-
import os
import httpretty
import pytest

from stw_potsdam.swp_webspeiseplan_api import SWPWebspeiseplanAPI


@pytest.fixture
def api_offline():
    """Disallow all network requests."""
    httpretty.enable(allow_net_connect=False)
    yield
    httpretty.disable()
    httpretty.reset()


@pytest.fixture
def api_online_one_shot():
    """Allow a single API request, returning the contents of 'input.json'.

    Subsequent API invocations will return with HTTP status code 500.
    """
    # pylint: disable=unused-argument
    def canned_menu(request, uri, response_headers):
        path = os.path.join(os.path.dirname(__file__),
                            'resources', 'input.json')

        with open(path, encoding='utf-8') as api_response:
            return 200, response_headers, api_response.read()

    responses = [
        httpretty.Response(body=canned_menu),
        httpretty.Response(body='invalid', status=500),
    ]

    httpretty.register_uri(httpretty.POST,
                           SWPWebspeiseplanAPI.URL_BASE,
                           responses=responses)

    httpretty.enable(allow_net_connect=False)
    yield httpretty
    httpretty.disable()
    httpretty.reset()
