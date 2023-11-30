from xml.dom import minidom
from datetime import date


class Builder:
    """A class method for creating a new class."""

    def __init__(self):
        """Initialize the object for the OpenMensa Feed Doc XML."""
        self._doc = minidom.Document()
        self._om = self._doc.createElement("openmensa")
        self._om.setAttribute("version", "2.1")
        self._om.setAttribute("xmlns", "http://openmensa.org/open-mensa-v2")
        self._om.setAttribute(
            "xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance"
        )
        self._om.setAttribute(
            "xsi:schemaLocation",
            "http://openmensa.org/open-mensa-v2 "
            + "http://openmensa.org/open-mensa-v2.xsd",
        )
        self._version = None
        self._name = None
        self._address = None
        self._city = None
        self._phone = None
        self._email = None
        self._location = None
        self._availability = None
        self._times = None
        self._feed = None
        self._day = None
        self._days: dict[date, dict[str, list]] = {}

    @property
    def version(self):
        """The version of the device .

        Returns:
            [type]: [description]
        """
        return self._version

    @version.setter
    def version(self, value: str):
        self._version = value

    @version.deleter
    def version(self):
        del self._version

    @property
    def name(self):
        """Name of the canteen .

        Returns:
            [type]: [description]
        """
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @name.deleter
    def name(self):
        del self._name

    @property
    def address(self):
        """The address of the canteen .

        Returns:
            [type]: [description]
        """
        return self._address

    @address.setter
    def address(self, value: tuple[str, str, str]):
        street_nr, zip_code, city = value
        self._address = f"{street_nr}, {zip_code} {city}"

    @address.deleter
    def address(self):
        del self._address

    @property
    def city(self):
        """Get the city of the canteen .

        Returns:
            [type]: [description]
        """
        return self._city

    @city.setter
    def city(self, value: str):
        self._city = value

    @city.deleter
    def city(self):
        del self._city

    @property
    def phone(self):
        """The phone number .

        Returns:
            [type]: [description]
        """
        return self._phone

    @phone.setter
    def phone(self, value: str):
        self._phone = value

    @phone.deleter
    def phone(self):
        del self._phone

    @property
    def email(self):
        """The email address of the canteen .

        Returns:
            [type]: [description]
        """
        return self._email

    @email.setter
    def email(self, value: str):
        self._email = value

    @email.deleter
    def email(self):
        del self._email

    @property
    def location(self):
        """Get a tuple containing the location as latitude and longitude .

        Returns:
            [type]: [description]
        """
        return (self._longitude, self._latitude)

    @location.setter
    def location(self, value: tuple[float, float]):
        self._longitude = value[0]
        self._latitude = value[1]

    @location.deleter
    def location(self):
        del self._longitude
        del self._latitude

    @property
    def availability(self):
        """Whether the canteen is public or restriced.

        Returns:
            [type]: [description]
        """
        return self._availability

    @availability.setter
    def availability(self, value: str):
        if value == "pulbic" or value == "restricted":
            self._availability = value
        else:
            raise ValueError("only 'public' or 'restricted are allowed.")

    @availability.deleter
    def availability(self):
        del self._availability

    @property
    def times(self):
        """Get the opening times the canteen.

        Returns:
            [type]: [description]
        """
        return self._times

    @times.setter
    def times(self, value: dict[str, str]):
        def attach_weekday(tag: str, value: str):
            """Attach a week tag to the week .

            Args:
                tag (str): [description]
                value (str): [description]
            """
            if value == "":
                return
            d = self._doc.createElement(tag)
            if value == "geschlossen":
                d.setAttribute("closed", "true")
            else:
                d.setAttribute("open", value)
            self._times.appendChild(d)

        weekdays = (
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
        )
        self._times = self._doc.createElement("times")
        self._times.setAttribute("type", "opening")

        for weekday in weekdays:
            v = value.get(weekday)
            if v:
                attach_weekday(weekday, v)

    @times.deleter
    def times(self):
        del self._times

    @property
    def feed(self):
        """Get a feed object .

        Returns:
            [type]: [description]
        """
        return self._feed

    @feed.setter
    def feed(self, value: dict):
        """Set the feed element .

        Args:
            value (dict): [description]
        """
        name: str = value.get("name")
        priority: int = value.get("priority")
        url: str = value.get("url")
        source: str = value.get("source")
        hour: int = value.get("hour")
        dayOfMonth: int | str = (
            value.get("dayOfMonth") if value.get("dayOfMonth") else "*"
        )
        dayOfWeek: int | str = (
            value.get("dayOfWeek") if value.get("dayOfWeek") else "*"
        )
        month: int | str = value.get("month") if value.get("month") else "*"
        minute: int = value.get("minute") if value.get("minute") else 0
        retry: str = value.get("retry")

        self._feed = self._doc.createElement("feed")
        self._feed.setAttribute("name", name)
        self._feed.setAttribute("priority", str(priority))
        schedule = self._doc.createElement("schedule")
        self._feed.appendChild(schedule)
        schedule.setAttribute("dayOfMonth", str(dayOfMonth))
        schedule.setAttribute("dayOfWeek", str(dayOfWeek))
        schedule.setAttribute("month", str(month))
        schedule.setAttribute("hour", str(hour))
        schedule.setAttribute("minute", str(minute))
        if retry:
            schedule.setAttribute("retry", retry)

        el = self._doc.createElement("url")
        self._feed.appendChild(el)
        node = self._doc.createTextNode(url)
        el.appendChild(node)

        el = self._doc.createElement("source")
        self._feed.appendChild(el)
        node = self._doc.createTextNode(source)
        el.appendChild(node)

    @feed.deleter
    def feed(self):
        del self._feed

    @property
    def day(self):
        """Returns the number of day of the week .

        Returns:
            [type]: [description]
        """
        return self._day

    @day.setter
    def day(self, value):
        self._day = value

    @day.deleter
    def day(self):
        del self._day

    def add_meal(
        self,
        date: date,
        category: str,
        name: str,
        prices: dict[str, float],
        note: str = None,
    ):
        """Add a meal element to the document .

        Args:
            date (date): [description]
            category (str): [description]
            name (str): [description]
            prices (dict[str, float]): [description]
            note (str, optional): [description]. Defaults to None.
        """
        meal = self._doc.createElement("meal")
        node = self._doc.createElement("name")
        meal.appendChild(node)
        data = self._doc.createTextNode(name)
        node.appendChild(data)

        if note:
            node = self._doc.createElement("note")
            meal.appendChild(node)
            data = self._doc.createTextNode(note)
            node.appendChild(data)

        if prices["student"]:
            node = self._doc.createElement("price")
            meal.appendChild(node)
            node.setAttribute("role", "student")
            data = self._doc.createTextNode(f'{prices["student"]:.2f}')
            node.appendChild(data)
        if prices["employee"]:
            node = self._doc.createElement("price")
            meal.appendChild(node)
            node.setAttribute("role", "employee")
            data = self._doc.createTextNode(f'{prices["employee"]:.2f}')
            node.appendChild(data)

        if prices["other"]:
            node = self._doc.createElement("price")
            meal.appendChild(node)
            node.setAttribute("role", "other")
            data = self._doc.createTextNode(f'{prices["other"]:.2f}')
            node.appendChild(data)

        category_dict = self._days.get(date, dict())
        if not category_dict:
            self._days[date] = category_dict
        meal_list = category_dict.get(category, list())
        if not meal_list:
            category_dict[category] = meal_list
        meal_list.append(meal)

    def __append_node(self, tag: str, value: str):
        """Create a node with a tag and text .

        Args:
            tag (str): [description]
            value (str): [description]
        """
        elem = self._doc.createElement(tag)
        self._canteen.appendChild(elem)
        node = self._doc.createTextNode(value)
        elem.appendChild(node)

    def toXML(self):
        """Return a XML string representing the canteen.

        Returns:
            [type]: [description]
        """
        self._doc.appendChild(self._om)
        if self.version:
            self.__append_node("version", self.version)
        self._canteen = self._doc.createElement("canteen")
        self._om.appendChild(self._canteen)
        if self.name:
            self.__append_node("name", self.name)
        if self.address:
            self.__append_node("address", self.address)
        if self.city:
            self.__append_node("city", self.city)
        if self.phone:
            self.__append_node("phone", self.phone)
        if self.email:
            self.__append_node("email", self.email)
        if self._longitude and self._latitude:
            location = self._doc.createElement("location")
            self._canteen.appendChild(location)
            location.setAttribute("latitude", str(self._latitude))
            location.setAttribute("longitude", str(self._longitude))
        if self.availability:
            self.__append_node("availability", self.availability)
        if self.times:
            self._canteen.appendChild(self.times)
        if self.feed:
            self._canteen.appendChild(self.feed)

        for date, category_dict in sorted(self._days.items()):
            day = self._doc.createElement("day")
            self._canteen.appendChild(day)
            day.setAttribute("date", str(date))
            for category_name, meals in sorted(category_dict.items()):
                category = self._doc.createElement("category")
                day.appendChild(category)
                category.setAttribute("name", category_name)
                for meal in meals:
                    category.appendChild(meal)
        return self._doc.toprettyxml(encoding="UTF-8")
