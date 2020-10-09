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
        if isinstance(price, str) and price.strip():
            result[role] = price

    return result


def _process_day(builder, day):
    for offer in _offers(day):
        builder.addMeal(date=day['data'],
                        category=offer['titel'],
                        name=offer['beschreibung'],
                        notes=_notes(offer),
                        prices=_prices(offer),
                        roles=None)


def _offers(day):
    offers = day['angebote']
    if isinstance(offers, list):
        return offers

    if isinstance(offers, dict):
        # allows for the following structure:
        # {'-1': <garbage>, '0': first_offer, ...}
        # This case is degenerate and occurs only on semi-regular basis
        # as of 2020-10-20. The assumption that offers at logical index -1
        # are garbage can be challenged, it is simply a result of observing
        # the API responses over several months.
        return [offer for index, offer in offers.items() if int(index) >= 0]

    raise AssertionError(f'cannot handle offers of type {type(offers)}')


def render_menu(menu):
    """Render the menu for a canteen into an OpenMensa XML feed.

    :param dict menu: the Python representation of the API JSON response
    :return: the XML feed as string
    """
    builder = LazyBuilder()

    if menu:
        for day in _active_days(menu):
            _process_day(builder, day)

    return builder.toXMLFeed()


def render_meta(canteen, menu_feed_url):
    """Render a OpenMensa XML meta feed for a given canteen.

    :param Canteen canteen: the canteen
    :param menu_feed_url: the canteen menu URL
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
