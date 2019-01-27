# -*- encoding: utf-8 -*-

import ConfigParser
import io
import os
from functools import partial
from stw_potsdam.canteen import Canteen


def _get_config(filename):
    config = ConfigParser.SafeConfigParser()
    path = os.path.join(os.path.dirname(__file__), filename)
    with io.open(path, encoding='utf-8') as config_file:
        config.readfp(config_file)
    return config


def _parse_canteen(config, canteen_name):
    get = partial(config.get, canteen_name)
    return Canteen(key=canteen_name,
                   name=get('name'),
                   street=get('street'),
                   city=get('city'),
                   id=get('id'),
                   chash=get('cHash'))


def read_canteen_config():
    config = _get_config('canteens.ini')
    return {name: _parse_canteen(config, name) for name in config.sections()}
