# -*- encoding: utf-8 -*-

import json
from collections import namedtuple
import requests

MenuParams = namedtuple('MenuParams', ('canteen_id', 'chash'))

URL = 'https://www.studentenwerk-potsdam.de' + \
      '/essen/unsere-mensen-cafeterien/detailinfos/'


def _param_json(to_serialize):
    """Obtain JSON string of an object without whitespace on delimiters.

    :param dict it: The data structure to serialize
    :return: JSON string, no whitespace between separators
    """
    return json.dumps(to_serialize, separators=(',', ':'))


def download_menu(menu_params):
    """Download the menu for a specific canteen.

    :param MenuParams menu_params: the target canteen
    """
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
