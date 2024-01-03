import logging
from datetime import datetime, date
from stw_potsdam.xml_types.canteen_xml import CanteenMeta, CanteenXML
from stw_potsdam.xml_types.times_xml import CanteenOpenTimespec, TimesXML
from stw_potsdam.xml_types.meal_xml import MealXML


class SWPWebspeiseplanParser:
    """Class method to parse SWP_Webspeiseplan."""

    def __init__(self) -> None:
        """Init SWPWebspeiseplanParser object."""
        logging.basicConfig()
        self.logger = logging.getLogger(__name__)

    def parse_canteen_meta_times(self, outlet: dict):
        """Parse the outlet data from outlet.

        Args:
            outlet (dict): [description]
        """
        self.logger.debug("parse_canteen_meta_times(): %s", outlet["name"])
        addr_info = outlet["addressInfo"]
        meta = {
            "name": outlet["name"],
            "address": f'{addr_info["street"]}, {addr_info["postalCode"]} '
            + f'{addr_info["city"]}',
            "city": addr_info["city"],
            "phone": outlet["contactInfo"][0]["phone"],
            "email": outlet["contactInfo"][0]["email"],
            "availability": outlet["isPublic"]
        }

        if outlet["positionInfo"]:
            meta["location"] = (
                outlet["positionInfo"]["longitude"],
                outlet["positionInfo"]["latitude"],
            )
        canteen_meta = CanteenMeta(**meta)
        weekday_dict = {
            # this approach only lists the first (valid) opening time,
            # since OpenMensa does not support multiple time specs
            # (yet).
            "monday": outlet['moZeit1'] or outlet['moZeit2'],
            "tuesday": outlet['diZeit1'] or outlet['diZeit2'],
            "wednesday": outlet['miZeit1'] or outlet['miZeit2'],
            "thursday": outlet['doZeit1'] or outlet['doZeit2'],
            "friday": outlet['frZeit1'] or outlet['frZeit2'],
            "saturday": outlet['saZeit1'] or outlet['saZeit2'],
            "sunday": outlet['soZeit1'] or outlet['soZeit2'],
        }

        canteen_times = TimesXML({
            k: CanteenOpenTimespec(v) for k, v in weekday_dict.items()
        })
        canteen = CanteenXML(canteen_meta, canteen_times)
        return canteen

    def parse_meals(
        self, menu_data, meal_categories
    ) -> list[tuple[date, str, MealXML]]:
        """Parse the menu and adds it to the builder."""
        meals = []
        for menu in menu_data:
            for meal_data in menu["speiseplanGerichtData"]:
                info = meal_data["speiseplanAdvancedGericht"]
                additional_info = meal_data["zusatzinformationen"]
                price = {
                    "student": additional_info["mitarbeiterpreisDecimal2"],
                    "employee": additional_info["price3Decimal2"],
                    "other": additional_info["gaestepreisDecimal2"],
                }
                meal = MealXML(name=info["gerichtname"], price=price)
                day = datetime.fromisoformat(info["datum"]).date()
                category = meal_categories[info["gerichtkategorieID"]]["name"]
                meals.append(
                    {"day": day, "category": category, "meal": meal}
                )
        self.logger.debug("parse_meals(): %s meals parsed", len(meals))
        return meals
