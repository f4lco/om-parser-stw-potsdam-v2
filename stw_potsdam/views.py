# -*- encoding: utf-8 -*-

from flask import Flask, make_response
from werkzeug.contrib.cache import SimpleCache

import feed
from config import read_canteen_config
from canteen_api import MenuParams, download_menu

CACHE_TIMEOUT = 45 * 60

app = Flask(__name__)
app.url_map.strict_slashes = False

cache = SimpleCache()


def canteen_not_found(config, canteen_name):
    app.logger.warn('Canteen %s not found', canteen_name)
    configured = ', '.join("'{}'".format(c) for c in config.keys())
    message = "Canteen '{canteen}' not found, available: {configured}".format(canteen=canteen_name,
                                                                              configured=configured)
    return make_response(message, 404)


def get_menu_cached(canteen):
    params = MenuParams(canteen_id=canteen.id, chash=canteen.chash)
    menu = cache.get(params)
    if menu:
        app.logger.info('Using cached menu for %s', canteen)
    return menu or get_menu(canteen, params)


def get_menu(canteen, params):
    app.logger.info('Downloading menu for %s', canteen)
    menu = download_menu(params)
    cache.set(params, menu, timeout=CACHE_TIMEOUT)
    return menu


def _canteen_feed_xml(xml):
    response = make_response(xml)
    response.mimetype = 'text/xml'
    return response


def canteen_menu_feed_xml(canteen, menu):
    xml = feed.render_menu(canteen, menu)
    return _canteen_feed_xml(xml)


def canteen_meta_feed_xml(canteen, menu):
    xml = feed.render_meta(canteen, menu)
    return _canteen_feed_xml(xml)


@app.route('/canteens/<canteen_name>')
@app.route('/canteens/<canteen_name>/meta')
def canteen_meta_feed(canteen_name):
    config = read_canteen_config()

    if canteen_name not in config:
        return canteen_not_found(config, canteen_name)

    canteen = config[canteen_name]
    menu = get_menu_cached(canteen)
    return canteen_meta_feed_xml(canteen, menu)


@app.route('/canteens/<canteen_name>/menu')
def canteen_menu_feed(canteen_name):
    config = read_canteen_config()

    if canteen_name not in config:
        return canteen_not_found(config, canteen_name)

    canteen = config[canteen_name]
    menu = get_menu_cached(canteen)
    return canteen_menu_feed_xml(canteen, menu)


@app.route('/')
@app.route('/canteens')
def canteen_index():
    config = read_canteen_config()

    index_json = feed.render_index(config)

    response = make_response(index_json)
    response.mimetype = 'application/json'
    return response

