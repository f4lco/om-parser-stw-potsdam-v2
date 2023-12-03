from dataclasses import dataclass
from xml.dom import minidom
from datetime import date
from stw_potsdam.xml_types.times_xml import TimesXML
from stw_potsdam.xml_types.meal_xml import MealXML
from stw_potsdam.xml_types.feed_xml import FeedXML


@dataclass
class CanteenMeta:
    """Metadata for CanteenXML."""

    # pylint: disable=too-many-instance-attributes
    def __init__(self, **kwargs):
        """Init CanteenMeta object."""
        self.name: str = kwargs["name"]
        self.address: str = kwargs["address"]
        self.city: str = kwargs["city"]
        self.phone: str = kwargs["phone"]
        self.email = kwargs["email"]
        self.location: tuple[float, float] = kwargs.get("location", None)
        self.availability: str = kwargs.get("availability", "public")

    @property
    def availability(self) -> str:
        """Whether the canteen is public or restricted.

        Returns:
            str: 'public' | 'restricted'
        """
        return self._availability

    @availability.setter
    def availability(self, value: str):
        if value is True:
            self._availability = "public"
        elif value is False:
            self._availability = "restricted"
        elif value in ("public", "restricted"):
            self._availability = value
        else:
            raise ValueError("only 'public' or 'restricted' are allowed.")

    @availability.deleter
    def availability(self):
        del self._availability


@dataclass
class CanteenXML:
    """Represents the canteen tag in openMensaFeedv2."""

    def __init__(
        self,
        canteen_meta: CanteenMeta,
        times: TimesXML,
        feeds: dict[str, FeedXML] = None,
        days: dict[date, dict[str, list[MealXML]]] = None,
    ):
        """Init CanteenXML Object.

        Args:
            name (str): _description_
            address (str): _description_
            city (str): _description_
            phone (str): _description_
            email (str): _description_
            location (tuple[float, float]): _description_
            availability (str): _description_
            times (TimesXML): _description_
        """
        self.canteen_meta = canteen_meta
        self.times = times
        self.feeds = {} if feeds is None else feeds
        self.days = {} if days is None else days

    def __create_node(self, doc: minidom.Document, tag: str, value: str):
        elem = doc.createElement(tag)
        txt_node = doc.createTextNode(value)
        elem.appendChild(txt_node)
        return elem

    def __append_meta(self, doc: minidom.Document, canteen: minidom.Element):
        name = self.__create_node(doc, "name", self.canteen_meta.name)
        canteen.appendChild(name)
        address = self.__create_node(doc, "address", self.canteen_meta.address)
        canteen.appendChild(address)
        city = self.__create_node(doc, "city", self.canteen_meta.city)
        canteen.appendChild(city)
        phone = self.__create_node(doc, "phone", self.canteen_meta.phone)
        canteen.appendChild(phone)
        email = self.__create_node(doc, "email", self.canteen_meta.email)
        canteen.appendChild(email)
        if self.canteen_meta.location:
            location = doc.createElement("location")
            location.setAttribute(
                "longitude", str(self.canteen_meta.location[0])
            )
            location.setAttribute(
                "latitude", str(self.canteen_meta.location[1])
            )
            canteen.appendChild(location)
        availability = self.__create_node(
            doc, "availability", self.canteen_meta.availability
        )
        canteen.appendChild(availability)
        times = self.times.xml_element(doc)
        canteen.appendChild(times)

    def add_feed(self, feed: FeedXML):
        """Add a feed to the canteen.

        Args:
            feed (FeedXML): _description_
        """
        self.feeds[feed.name] = feed

    def add_meal(self, day: date, category: str, meal: MealXML):
        """Add a meal to the canteen.

        Args:
            day (date): Offered date of meal.
            catrgory (str): Meal's category.
            meal (MealXML): The meal item.
        """
        categories = self.days.get(day, {})
        if not categories:
            self.days[day] = categories
        meals = categories.get(category, [])
        if not meals:
            categories[category] = meals
        meals.append(meal)

    def xml_element(self, doc: minidom.Document):
        """Return the XML representation.

        Args:
            doc (minidom.Document): Working XML document

        Returns:
            _type_: _description_
        """
        canteen = doc.createElement("canteen")
        self.__append_meta(doc, canteen)
        for feed_item in self.feeds.values():
            feed = feed_item.xml_element(doc)
            canteen.appendChild(feed)

        for day_data, categories in self.days.items():
            day = doc.createElement("day")
            day.setAttribute("date", str(day_data))
            for category_name, meals in categories.items():
                category = doc.createElement("category")
                category.setAttribute("name", category_name)
                for meal in meals:
                    category.appendChild(meal.xml_element(doc))
                day.appendChild(category)
            canteen.appendChild(day)
        return canteen
