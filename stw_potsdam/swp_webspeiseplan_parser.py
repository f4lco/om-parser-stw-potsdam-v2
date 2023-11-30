import logging
from datetime import datetime
from stw_potsdam.builder import Builder
from stw_potsdam.swp_webspeiseplan_api import SWP_Webspeiseplan_API


class SWP_Webspeiseplan_Parser:
    """Class method to parse SWP_Webspeiseplan."""

    def __init__(
        self,
        menu_data: list[dict],
        meal_categories: list[dict],
        outlet_data: dict,
        url: str,
    ):
        """Initialize the parser .

        Args:
            menu_data (list[dict]): [description]
            meal_categories (list[dict]): [description]
            outlet_data (dict): [description]
            url (str): [description]
        """
        logging.basicConfig()
        self.logger = logging.getLogger(__name__)
        self.menu_data = menu_data
        self.meal_categories = meal_categories
        self.outlet_data = outlet_data
        self.url = url
        self._builder = Builder()
        self.__parse_canteen(outlet_data)
        self.__parse_feed()
        self.__parse_meals()

    def __parse_canteen(self, outlet: dict):
        """Parse the outlet data from outlet.

        Args:
            outlet (dict): [description]
        """
        canteen = self._builder
        canteen.name = outlet["name"]
        canteen.address = (
            outlet["addressInfo"]["street"],
            outlet["addressInfo"]["postalCode"],
            outlet["addressInfo"]["city"],
        )
        canteen.city = outlet["addressInfo"]["city"]
        canteen.phone = outlet["contactInfo"][0]["phone"]
        canteen.email = outlet["contactInfo"][0]["email"]
        if outlet["positionInfo"]:
            canteen.location = (
                outlet["positionInfo"]["longitude"],
                outlet["positionInfo"]["latitude"],
            )

        # TODO: availability via locations isPublic

        times = {
            "monday": f"{outlet['moZeit1']}, {outlet['moZeit2']}",
            "tuesday": f"{outlet['diZeit1']}, {outlet['diZeit2']}",
            "wednesday": f"{outlet['miZeit1']}, {outlet['miZeit2']}",
            "thursday": f"{outlet['doZeit1']}, {outlet['doZeit2']}",
            "friday": f"{outlet['frZeit1']}, {outlet['frZeit2']}",
            "saturday": f"{outlet['saZeit1']}, {outlet['saZeit2']}",
            "sunday": f"{outlet['soZeit1']}, {outlet['soZeit2']}",
        }

        times = {
            k: v.replace("None, None", "")
            .replace("None,", "")
            .replace(", None", "")
            for k, v in times.items()
        }

        canteen.times = times

    def __parse_feed(self):
        """Parse feed and set feed."""
        feed = {
            "name": "full",
            "priority": 0,
            "hour": "8-14",
            "retry": "30 1",
            "url": self.url,
            "source": SWP_Webspeiseplan_API.URL_BASE,
        }
        self._builder.feed = feed

    def __parse_meals(self):
        """Parse the menu and adds it to the builder."""
        for menu in self.menu_data:
            for meal in menu["speiseplanGerichtData"]:
                info = meal["speiseplanAdvancedGericht"]
                date = datetime.fromisoformat(info["datum"]).date()
                additional_info = meal["zusatzinformationen"]
                self._builder.add_meal(
                    date=date,
                    category=self.meal_categories[info["gerichtkategorieID"]][
                        "name"
                    ],
                    name=info["gerichtname"],
                    prices={
                        "student": additional_info["mitarbeiterpreisDecimal2"],
                        "employee": additional_info["price3Decimal2"],
                        "other": additional_info["gaestepreisDecimal2"],
                    },
                )

    @property
    def xml_feed(self):
        """Return the XML string of the builder.

        Returns:
            [type]: [description]
        """
        return self._builder.toXML()
