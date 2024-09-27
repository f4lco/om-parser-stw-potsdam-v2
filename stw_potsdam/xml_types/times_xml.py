import re

from dataclasses import dataclass
from xml.dom import minidom


class CanteenOpenTimespec(str):
    """Represents valid daily opening times in openMensaFeedv2."""

    CLOSED = "geschlossen"
    CLOSED_VALID_VALUES = {
        CLOSED,
        None,
        False,
        "",
    }

    PATTERN = (r'.*(?P<hour1>\d{1,2}):(?P<min1>\d{1,2})'
               r'\D*(?P<hour2>\d{1,2}):(?P<min2>\d{1,2}).*')
    
    MATCHER = re.compile(PATTERN)

    def __new__(cls, spec):
        """Create CanteenOpenTimespec object.

        Args:
            spec (str | bool | None): time specification
        """
        if spec in cls.CLOSED_VALID_VALUES:
            return super().__new__(cls, cls.CLOSED)

        match = cls.MATCHER.match(str(spec))
        if not match:
            raise ValueError(f'Invalid time specification: {spec!r} does'
                             f' not conform to regex {cls.PATTERN!r}')
        # parse to int for format zerofill
        int_spec = {k: int(v) for k, v in match.groupdict().items()}
        clean_spec = (
            f'{int_spec["hour1"]:02}:{int_spec["min1"]:02}-'
            f'{int_spec["hour2"]:02}:{int_spec["min2"]:02}'
        )
        return super().__new__(cls, clean_spec)


@dataclass
class TimesXML:
    """Represents the times tag in openMensaFeedv2."""

    VALID_DAYS = (
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    )

    monday: str
    tuesday: str
    wednesday: str
    thursday: str
    friday: str
    saturday: str
    sunday: str

    def __init__(self, weekday_dict: dict[str, CanteenOpenTimespec] = None):
        """Init TimesXML object.

        Args:
            weekday_dict (dict[str, str]): _description_
        """
        for key in weekday_dict:
            if key in self.VALID_DAYS:
                setattr(self, key, weekday_dict[key])
            else:
                raise KeyError()

    def __create_node(
        self, doc: minidom.Document, tag: str, value: CanteenOpenTimespec
    ):
        elem = doc.createElement(tag)
        if value in CanteenOpenTimespec.CLOSED_VALID_VALUES:
            elem.setAttribute("closed", "true")
        else:
            elem.setAttribute("open", value)
        return elem

    def xml_element(self, doc: minidom.Document):
        """Return the XML representation.

        Args:
            doc (minidom.Document): Working XML document

        Returns:
            _type_: _description_
        """
        times = doc.createElement("times")
        times.setAttribute("type", "opening")

        for day in self.VALID_DAYS:
            day_node = self.__create_node(doc, day, getattr(self, day))
            times.appendChild(day_node)

        return times
