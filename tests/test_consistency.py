# -*- encoding: utf-8 -*-

import io
import json
import os

from stw_potsdam import feed
from stw_potsdam.config import read_canteen_config


def _resource_path(filename):
    return os.path.join('tests', 'resources', filename)


def _canteen():
    return read_canteen_config()['griebnitzsee']


def _menu():
    with open(_resource_path('input.json')) as f:
        return json.load(f)


def _expected_meta_feed():
    with io.open(_resource_path('meta_output.xml'), encoding='utf-8') as f:
        return f.read()


def _expected_menu_feed():
    with io.open(_resource_path('menu_output.xml'), encoding='utf-8') as f:
        return f.read()


def test_meta_consistency():
    canteen = _canteen()
    menu = _menu()

    actual = feed.render_meta(canteen, menu)

    expected = _expected_meta_feed()
    assert expected == actual


def test_menu_consistency():
    canteen = _canteen()
    menu = _menu()

    actual = feed.render_menu(menu)

    expected = _expected_menu_feed()
    assert expected == actual
