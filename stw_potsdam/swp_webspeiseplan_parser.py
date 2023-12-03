import logging
from datetime import datetime, date
from stw_potsdam.xml_types.canteen_xml import CanteenMeta, CanteenXML
from stw_potsdam.xml_types.times_xml import TimesXML
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
        }

        if outlet["positionInfo"]:
            meta["location"] = (
                outlet["positionInfo"]["longitude"],
                outlet["positionInfo"]["latitude"],
            )
        canteen_meta = CanteenMeta(**meta)
        # TODO: availability via locations isPublic
        weekday_dict = {
            "monday": f"{outlet['moZeit1']}, {outlet['moZeit2']}",
            "tuesday": f"{outlet['diZeit1']}, {outlet['diZeit2']}",
            "wednesday": f"{outlet['miZeit1']}, {outlet['miZeit2']}",
            "thursday": f"{outlet['doZeit1']}, {outlet['doZeit2']}",
            "friday": f"{outlet['frZeit1']}, {outlet['frZeit2']}",
            "saturday": f"{outlet['saZeit1']}, {outlet['saZeit2']}",
            "sunday": f"{outlet['soZeit1']}, {outlet['soZeit2']}",
        }

        weekday_dict = {
            k: v.replace("None, None", "")
            .replace("None,", "")
            .replace(", None", "")
            for k, v in weekday_dict.items()
        }

        canteen_times = TimesXML(weekday_dict)
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
