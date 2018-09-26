# -*- encoding: utf-8 -*-

from pyopenmensa.feed import LazyBuilder


PRICE_ROLE_MAPPING = {
    'student': 'preis_s',
    'other': 'preis_g',
    'employee': 'preis_m'
}


def _active_days(menu):
    for container in menu['wochentage']:
        day = container['datum']
        active = 'angebote' in day
        if active:
            yield day


def _notes(offer):
    result = []
    for label in offer['labels']:
        result.append(label['name'].capitalize())
    return result


def _prices(offer):
    result = {}
    for role, api_role in PRICE_ROLE_MAPPING.items():
        if api_role not in offer:
            continue

        price = offer[api_role]
        # When no price is set, this can be empty dict
        if isinstance(price, (unicode, str)) and price.strip():
            # Convert unicode to str for PyOpenMensa -> misses type check
            result[role] = str(price)

    return result


def _process_day(builder, day):
    for offer in day['angebote']:
        builder.addMeal(date=day['data'],
                        category=offer['titel'],
                        name=offer['beschreibung'],
                        notes=_notes(offer),
                        prices=_prices(offer),
                        roles=None)


def render_menu(menu):
    """Render the menu for a canteen into an OpenMensa XML feed.

    :param dict menu: the Python representation of the API JSON response
    :return: the XML feed as string
    """
    builder = LazyBuilder()

    for day in _active_days(menu):
        _process_day(builder, day)

    return builder.toXMLFeed()


def render_meta(canteen, menu_feed_url):
    """Render a OpenMensa XML meta feed for a given canteen.

    :param Canteen canteen: the canteen
    :return: the XML meta feed as string
    """
    builder = LazyBuilder()

    builder.name = canteen.name
    builder.address = canteen.street
    builder.city = canteen.city

    builder.define(name='full',
                   priority='0',
                   url=menu_feed_url,
                   source=None,
                   dayOfWeek='*',
                   dayOfMonth='*',
                   hour='8-18',
                   minute='0',
                   retry='30 1')

    return builder.toXMLFeed()
