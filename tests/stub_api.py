# -*- encoding: utf-8 -*-
import os
import re
import httpretty
import pytest


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

    def make_handler(filename):
        path = os.path.join(
            os.path.dirname(__file__),
            'resources',
            'integration-test',
            filename,
        )

        # pylint: disable=unused-argument
        def handle(request, uri, response_headers):
            with open(path, encoding='utf-8') as api_response:
                return 200, response_headers, api_response.read()

        return handle

    httpretty.register_uri(
        httpretty.GET,
        "https://swp.webspeiseplan.de",
        responses=[
            httpretty.Response(body=make_handler('index.html')),
            httpretty.Response(body='invalid', status=500),
        ],
    )

    httpretty.register_uri(
        httpretty.GET,
        'https://swp.webspeiseplan.de/main.b25ba5c971eb2b45f391.js',
        responses=[
            httpretty.Response(body=make_handler("snippet.js")),
        ])

    httpretty.register_uri(
        httpretty.GET,
        re.compile(r'.*index.php.*model=outlet.*'),
        match_querystring=True,
        responses=[
            httpretty.Response(body=make_handler('outlets.json')),
        ],
    )

    httpretty.register_uri(
        httpretty.GET,
        re.compile(r'.*index.php.*model=location.*'),
        match_querystring=True,
        responses=[
            httpretty.Response(body=make_handler('location.json')),
        ],
    )

    httpretty.register_uri(
        httpretty.GET,
        re.compile(r'.*index.php.*model=menu.*'),
        match_querystring=True,
        responses=[
            httpretty.Response(body=make_handler("menu.json")),
        ]
    )

    httpretty.register_uri(
        httpretty.GET,
        re.compile(r'.*index.php.*model=mealCategory.*'),
        match_querystring=True,
        responses=[
            httpretty.Response(body=make_handler('meal_category.json')),
        ]
    )

    httpretty.enable(allow_net_connect=False)
    yield httpretty
    httpretty.disable()
    httpretty.reset()
