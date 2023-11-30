# -*- encoding: utf-8 -*-

import os
import urllib.parse

import cachetools as ct

from flask import Flask, jsonify, make_response, url_for
from flask.logging import create_logger

from stw_potsdam.config import read_canteen_config
from stw_potsdam.swp_webspeiseplan_api import SWP_Webspeiseplan_API
from stw_potsdam.swp_webspeiseplan_parser import SWP_Webspeiseplan_Parser

CACHE_TIMEOUT = 45 * 60

# pragma pylint: disable=invalid-name

app = Flask(__name__)
app.url_map.strict_slashes = False

log = create_logger(app)

if "BASE_URL" in os.environ:  # pragma: no cover
    base_url = urllib.parse.urlparse(os.environ.get("BASE_URL"))
    if base_url.scheme:
        app.config["PREFERRED_URL_SCHEME"] = base_url.scheme
    if base_url.netloc:
        app.config["SERVER_NAME"] = base_url.netloc
    if base_url.path:
        app.config["APPLICATION_ROOT"] = base_url.path

cache = ct.TTLCache(maxsize=30, ttl=CACHE_TIMEOUT)


def canteen_not_found(config, canteen_name):
    log.warning("Canteen %s not found", canteen_name)
    configured = ", ".join(f"'{c}'" for c in config.keys())
    message = f"Canteen '{canteen_name}' not found, available: {configured}"
    return make_response(message, 404)


@ct.cached(cache=cache)
def get_menu():
    log.debug("Downloading menu for SWP")
    return SWP_Webspeiseplan_API()


@app.route("/canteens/<canteen_name>")
@app.route("/canteens/<canteen_name>/xml")
def canteen_xml_feed(canteen_name):
    config = read_canteen_config()

    if canteen_name not in config:
        return canteen_not_found(config, canteen_name)

    canteen = config[canteen_name]
    swp_api = get_menu()
    swp_parser = SWP_Webspeiseplan_Parser(
        swp_api.menus[canteen.name],
        swp_api.meal_categories[canteen.name],
        swp_api.outlets[canteen.name],
        url_for("canteen_xml_feed", canteen_name=canteen.key, _external=True),
    )
    xml = swp_parser.xml_feed.decode()
    response = make_response(xml)
    response.mimetype = "text/xml"
    return response


@app.route("/")
@app.route("/canteens")
def canteen_index():
    config = read_canteen_config()
    return jsonify(
        {
            key: url_for("canteen_xml_feed", canteen_name=key, _external=True)
            for key in config
        }
    )


@app.route("/health_check")
def health_check():
    return make_response("OK", 200)
