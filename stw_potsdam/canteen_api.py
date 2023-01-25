# -*- encoding: utf-8 -*-

import json
import logging
from collections import namedtuple
import requests

MenuParams = namedtuple('MenuParams', ('canteen_id', 'chash'))

URL = 'https://www.studentenwerk-potsdam.de' + \
      '/essen/unsere-mensen/detailinfos/'

LOG = logging.getLogger(__name__)


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
    params = {
        'tx_ddfmensa_ddfmensajson[interneid]': menu_params.canteen_id,
        'type': 14529821235,
        'cHash': menu_params.chash
    }

    body = {
        'data': False
    }

    request = requests.post(URL, params=params, json=body, timeout=30)

    # urllib3 does not log response bodies - requests no longer supports it:
    # https://2.python-requests.org//en/master/api/#api-changes
    LOG.debug('Response:\n>>>>>\n%s\n<<<<<', request.text)

    return request.json()
