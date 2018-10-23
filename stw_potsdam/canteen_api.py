# -*- encoding: utf-8 -*-

import json
import requests
from collections import namedtuple

MenuParams = namedtuple('MenuParams', ('canteen_id', 'chash'))

URL = 'https://www.studentenwerk-potsdam.de' + \
      '/essen/unsere-mensen-cafeterien/detailinfos/'


def _param_json(it):
    return json.dumps(it, separators=(',', ':'))


def download_menu(menu_params):
    context = {
        'record': 'pages_66',
        'path': 'tt_content.list.20.ddfmensa_ddfmensajson'
    }

    params = {
        'tx_typoscriptrendering[context]': _param_json(context),
        'tx_ddfmensa_ddfmensajson[mensa]': menu_params.canteen_id,
        'cHash': menu_params.chash
    }

    body = {
        'data': False
    }

    request = requests.post(URL, params=params, json=body)
    return request.json()
