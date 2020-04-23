# -*- encoding: utf-8 -*-

import os
import urllib.parse

import cachetools as ct

from flask import Flask, jsonify, make_response, url_for
from flask.logging import create_logger

from stw_potsdam import feed
from stw_potsdam.config import read_canteen_config
from stw_potsdam.canteen_api import MenuParams, download_menu

CACHE_TIMEOUT = 45 * 60

# pragma pylint: disable=invalid-name

app = Flask(__name__)
app.url_map.strict_slashes = False

log = create_logger(app)

if 'BASE_URL' in os.environ:  # pragma: no cover
    base_url = urllib.parse.urlparse(os.environ.get('BASE_URL'))
    if base_url.scheme:
        app.config['PREFERRED_URL_SCHEME'] = base_url.scheme
    if base_url.netloc:
        app.config['SERVER_NAME'] = base_url.netloc
    if base_url.path:
        app.config['APPLICATION_ROOT'] = base_url.path

cache = ct.ttl.TTLCache(maxsize=30, ttl=CACHE_TIMEOUT)


def canteen_not_found(config, canteen_name):
    log.warning('Canteen %s not found', canteen_name)
    configured = ', '.join("'{}'".format(c) for c in config.keys())
    message = "Canteen '{0}' not found, available: {1}".format(canteen_name,
                                                               configured)
    return make_response(message, 404)


def _menu_params(canteen):
    return MenuParams(canteen_id=canteen.id, chash=canteen.chash)


@ct.cached(cache=cache, key=_menu_params)
def get_menu(canteen):
    log.info('Downloading menu for %s', canteen)
    params = _menu_params(canteen)
    return download_menu(params)


def _canteen_feed_xml(xml):
    response = make_response(xml)
    response.mimetype = 'text/xml'
    return response


def canteen_menu_feed_xml(menu):
    xml = feed.render_menu(menu)
    return _canteen_feed_xml(xml)


def canteen_meta_feed_xml(canteen):
    menu_feed_url = url_for('canteen_menu_feed',
                            canteen_name=canteen.key,
                            _external=True)
    xml = feed.render_meta(canteen, menu_feed_url)
    return _canteen_feed_xml(xml)


@app.route('/canteens/<canteen_name>')
@app.route('/canteens/<canteen_name>/meta')
def canteen_meta_feed(canteen_name):
    config = read_canteen_config()

    if canteen_name not in config:
        return canteen_not_found(config, canteen_name)

    canteen = config[canteen_name]
    return canteen_meta_feed_xml(canteen)


@app.route('/canteens/<canteen_name>/menu')
def canteen_menu_feed(canteen_name):
    config = read_canteen_config()

    if canteen_name not in config:
        return canteen_not_found(config, canteen_name)

    canteen = config[canteen_name]
    menu = get_menu(canteen)
    return canteen_menu_feed_xml(menu)


@app.route('/')
@app.route('/canteens')
def canteen_index():
    config = read_canteen_config()
    return jsonify({
        key: url_for('canteen_meta_feed', canteen_name=key, _external=True)
        for key in config
    })


@app.route('/health_check')
def health_check():
    return make_response("OK", 200)
