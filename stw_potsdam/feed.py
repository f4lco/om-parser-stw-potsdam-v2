# -*- encoding: utf-8 -*-

from pyopenmensa.feed import LazyBuilder

from reverse import reverse

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
        if (isinstance(price, unicode) or isinstance(price, str)) and price.strip():
            result[role] = str(price)  # Convert unicode to str for PyOpenMensa -> misses type check

    return result


def _process_day(builder, day):
    for offer in day['angebote']:
        builder.addMeal(date=day['data'],
                        category=offer['titel'],
                        name=offer['beschreibung'],
                        notes=_notes(offer),
                        prices=_prices(offer),
                        roles=None)


def _create_builder(canteen, skip_meta=False):
    builder = LazyBuilder()

    if skip_meta is not True:
        builder.name = canteen.name
        builder.address = canteen.street
        builder.city = canteen.city

    return builder


def render_menu(canteen, menu):
    builder = _create_builder(canteen, skip_meta=True)

    for day in _active_days(menu):
        _process_day(builder, day)

    return builder.toXMLFeed()


def render_meta(canteen, menu):
    builder = _create_builder(canteen, skip_meta=False)

    menu_feed_url = reverse("canteens/{}/menu".format(canteen.key))
    builder.define(name="full", priority="0", url=menu_feed_url, source=None, dayOfWeek="*", dayOfMonth="*", hour="8-18", minute="0", retry="30 1")

    return builder.toXMLFeed()
