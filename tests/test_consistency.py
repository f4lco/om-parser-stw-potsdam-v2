# -*- encoding: utf-8 -*-

import io
import json
import os
import pytest

from stw_potsdam.config import read_canteen_config


def _resource_path(filename):
    return os.path.join(os.path.dirname(__file__), 'resources', filename)


def _canteen():
    return read_canteen_config()['griebnitzsee']


def _read_menu(resource_name):
    with open(_resource_path(resource_name), encoding='utf-8') as menu_file:
        return json.load(menu_file)


def _read_feed(resource_name):
    with io.open(_resource_path(resource_name), encoding='utf-8') as xml:
        return xml.read()

@pytest.mark.xfail(strict=True)
def test_meta_consistency():
    raise NotImplementedError()
    canteen = _canteen()
    menu_feed_url = f"canteens/{canteen.key}/xml"
    actual = feed.render_meta(canteen, menu_feed_url)
    expected = _read_feed('meta_output.xml')
    assert expected == actual

@pytest.mark.xfail(strict=True)
def test_menu_consistency():
    raise NotImplementedError()
    menu = _read_menu('input.json')
    actual = feed.render_menu(menu)
    expected = _read_feed('menu_output.xml')
    assert expected == actual

@pytest.mark.xfail(strict=True)
def test_empty_menu():
    raise NotImplementedError()
    menu = _read_menu('empty.json')
    actual = feed.render_menu(menu)
    expected = _read_feed('empty_menu_output.xml')
    assert expected == actual

@pytest.mark.xfail(strict=True)
def test_offers_dictionary():
    raise NotImplementedError()
    menu = _read_menu('offers-dict.json')
    actual = feed.render_menu(menu)
    expected = _read_feed('offers-dict-output.xml')
    assert expected == actual

@pytest.mark.xfail(strict=True)
def test_missing_category():
    raise NotImplementedError()
    menu = _read_menu('missing-category.json')
    actual = feed.render_menu(menu)
    expected = _read_feed('missing-category-output.xml')
    assert expected == actual
