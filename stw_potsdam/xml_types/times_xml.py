from dataclasses import dataclass
from xml.dom import minidom


@dataclass
class TimesXML:
    """Represents the times tag in openMensaFeedv2."""

    monday: str
    tuesday: str
    wednesday: str
    thursday: str
    friday: str
    saturday: str
    sunday: str

    def __init__(self, weekday_dict: dict[str, str] = None):
        """Init TimesXML object.

        Args:
            weekday_dict (dict[str, str]): _description_
        """
        for key in weekday_dict:
            if key in (
                "monday",
                "tuesday",
                "wednesday",
                "thursday",
                "friday",
                "saturday",
                "sunday",
            ):
                setattr(self, key, weekday_dict[key])
            else:
                raise KeyError()

    def __create_node(self, doc: minidom.Document, tag: str, value: str):
        e = doc.createElement(tag)
        if value == "geschlossen":
            e.setAttribute("closed", "true")
        else:
            e.setAttribute("open", value)
        return e

    def xml_element(self, doc: minidom.Document):
        """Return the XML representation.

        Args:
            doc (minidom.Document): Working XML document

        Returns:
            _type_: _description_
        """
        times = doc.createElement("times")
        times.setAttribute("type", "opening")
        monday = self.__create_node(doc, "monday", self.monday)
        times.appendChild(monday)
        tuesday = self.__create_node(doc, "tuesday", self.tuesday)
        times.appendChild(tuesday)
        wednesday = self.__create_node(doc, "wednesday", self.wednesday)
        times.appendChild(wednesday)
        thursday = self.__create_node(doc, "thursday", self.thursday)
        times.appendChild(thursday)
        friday = self.__create_node(doc, "friday", self.friday)
        times.appendChild(friday)
        saturday = self.__create_node(doc, "saturday", self.saturday)
        times.appendChild(saturday)
        sunday = self.__create_node(doc, "sunday", self.sunday)
        times.appendChild(sunday)
        return times
