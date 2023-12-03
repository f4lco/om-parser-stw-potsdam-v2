from xml.dom import minidom
from dataclasses import dataclass
from stw_potsdam.xml_types.canteen_xml import CanteenXML


@dataclass
class OpenMensaXML:
    """Represents the openmensa tag in openMensaFeedv2."""

    def __init__(self, version: str, canteen: CanteenXML):
        """Init OpenMensaXML.

        Args:
            version (str): Parser version
            canteen (CanteenXML): _description_
        """
        self.version = version
        self.canteen = canteen

    def __create_version_node(self, doc: minidom.Document):
        e = doc.createElement("version")
        tn = doc.createTextNode(self.version)
        e.appendChild(tn)
        return e

    def xml_element(self, doc: minidom.Document):
        """Create openmensa XML tag.

        Args:
            doc (minidom.Document): Working XML document

        Returns:
            _type_: _description_
        """
        om = doc.createElement("openmensa")
        om.setAttribute("version", "2.1")
        om.setAttribute("xmlns", "http://openmensa.org/open-mensa-v2")
        om.setAttribute(
            "xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance"
        )
        om.setAttribute(
            "xsi:schemaLocation",
            "http://openmensa.org/open-mensa-v2 "
            + "http://openmensa.org/open-mensa-v2.xsd",
        )

        version = self.__create_version_node(doc)
        om.appendChild(version)
        canteen = self.canteen.xml_element(doc)
        om.appendChild(canteen)
        return om
