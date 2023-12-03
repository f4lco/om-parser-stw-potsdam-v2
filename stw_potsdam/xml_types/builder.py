from xml.dom import minidom
from dataclasses import dataclass
import logging
from flask import url_for
from stw_potsdam.xml_types.openmensa_xml import OpenMensaXML
from stw_potsdam.swp_webspeiseplan_api import SWPWebspeiseplanAPI
from stw_potsdam.swp_webspeiseplan_parser import SWPWebspeiseplanParser
from stw_potsdam.config import Canteen
from stw_potsdam.xml_types.feed_xml import FeedXML, ScheduleXML


@dataclass
class Builder:
    """A class method for creating a new OpenMensa Feed."""

    VERSION = "2.0.1"

    def __init__(self, config: dict[str, Canteen]):
        """Initialize the object for the OpenMensa Feed Doc XML."""
        logging.basicConfig()
        self.logger = logging.getLogger(__name__)
        self._xml_data = {}
        swp_api = SWPWebspeiseplanAPI()
        swp_parser = SWPWebspeiseplanParser()
        for cname, ntup in config.items():
            if ntup.name not in swp_api.outlets.keys():
                self.logger.warning("%s not found in keys", ntup.name)
                continue
            outlet = swp_api.outlets[ntup.name]
            menus = swp_api.menus[ntup.name]
            categories = swp_api.meal_categories[ntup.name]
            locations = swp_api.locations[ntup.name]
            outlet["isPublic"] = locations["isPublic"]
            canteen = swp_parser.parse_canteen_meta_times(outlet)
            meals = swp_parser.parse_meals(menus, categories)
            for kwargs in meals:
                canteen.add_meal(**kwargs)
            feed = self.__create_feed(ntup)
            canteen.add_feed(feed)
            self._xml_data[cname] = OpenMensaXML(self.VERSION, canteen)

    def __create_feed(self, ntup: Canteen):
        schedule = ScheduleXML(
            hour="8-14",
            retry="30 1",
        )
        feed = FeedXML(
            name="full",
            priority=0,
            source=SWPWebspeiseplanAPI.URL_BASE,
            url=url_for(
                "canteen_xml_feed",
                canteen_name=ntup.key,
                _external=True,
            ),
            schedule=schedule,
        )
        return feed

    def get_xml(self, canteen_name: str):
        """Return a XML string representing the canteen.

        Returns:
            [type]: [description]
        """
        doc = minidom.Document()
        xml_element = self._xml_data[canteen_name].xml_element(doc)
        doc.appendChild(xml_element)
        return doc.toprettyxml(encoding="UTF-8")
