import logging
from pyopenmensa.feed import LazyBuilder
from datetime import datetime


class SWP_Webspeiseplan_Parser:
    def __init__(
        self, menu_data: list[dict], meal_categories: list[dict], outlet_data: dict
    ):
        logging.basicConfig()
        self.logger = logging.getLogger(__name__)
        self.menu_data = menu_data
        self.meal_categories = meal_categories
        self.outlet_data = outlet_data
        self.canteen = None
        self.__parse_canteen(outlet_data)
        self.__parse_meals()

    def __parse_canteen(self, outlet: dict):
        builder = LazyBuilder()
        builder.name = outlet["name"]
        builder.address = outlet["addressInfo"]["street"]
        builder.city = (
            f'{outlet["addressInfo"]["postalCode"]} {outlet["addressInfo"]["city"]}'
        )
        builder.phone = outlet["contactInfo"][0]["phone"]
        builder.email = outlet["contactInfo"][0]["email"]
        if outlet["positionInfo"]:
            builder.location(
                str(outlet["positionInfo"]["longitude"]),
                str(outlet["positionInfo"]["latitude"]),
            )

        builder.availability = f"Montag: {outlet['moZeit1']}, {outlet['moZeit2']}\n"
        builder.availability += f"Dienstag: {outlet['diZeit1']}, {outlet['diZeit2']}\n"
        builder.availability += f"Mittwoch: {outlet['miZeit1']}, {outlet['miZeit2']}\n"
        builder.availability += (
            f"Donnerstag: {outlet['doZeit1']}, {outlet['doZeit2']}\n"
        )
        builder.availability += f"Freitag: {outlet['frZeit1']}, {outlet['frZeit2']}\n"
        builder.availability += f"Samstag: {outlet['saZeit1']}, {outlet['saZeit2']}\n"
        builder.availability += f"Sonntag: {outlet['soZeit1']}, {outlet['soZeit2']}"
        builder.availability = (
            builder.availability.replace("None, None", "")
            .replace("None,", "")
            .replace(", None", "")
        )

        self.canteen = builder

    def __parse_meals(self):
        for menu in self.menu_data:
            for meal in menu["speiseplanGerichtData"]:
                info = meal["speiseplanAdvancedGericht"]
                date = datetime.fromisoformat(info["datum"]).date()

                additional_info = meal["zusatzinformationen"]
                self.canteen.addMeal(
                    date=date,
                    category=self.meal_categories[info["gerichtkategorieID"]]["name"],
                    name=info["gerichtname"],
                    prices={
                        "employee": f'{additional_info["mitarbeiterpreisDecimal2"]:.2f}',
                        "other": f'{additional_info["gaestepreisDecimal2"]:.2f}',
                    },
                )

    @property
    def xml_feed(self):
        return self.canteen.toXMLFeed()
