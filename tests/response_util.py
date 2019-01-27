# -*- encoding: utf-8 -*-
from xml.etree import ElementTree


def meal_names(response):
    """Extract meal names from OpenMensa XML.

    By no means below parsing is robust or complete. Below just helps ensuring that the parser indeed returns proper XML
    instead of arbitrary responses."""
    root = ElementTree.fromstring(response)
    namespace = {'om': 'http://openmensa.org/open-mensa-v2'}
    nodes = root.findall('om:canteen/om:day/om:category/om:meal/om:name', namespace)
    return [node.text for node in nodes]
