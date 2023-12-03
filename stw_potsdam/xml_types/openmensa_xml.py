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
        elem = doc.createElement("version")
        txt_node = doc.createTextNode(self.version)
        elem.appendChild(txt_node)
        return elem

    def xml_element(self, doc: minidom.Document):
        """Create openmensa XML tag.

        Args:
            doc (minidom.Document): Working XML document

        Returns:
            _type_: _description_
        """
        open_mensa = doc.createElement("openmensa")
        open_mensa.setAttribute("version", "2.1")
        open_mensa.setAttribute("xmlns", "http://openmensa.org/open-mensa-v2")
        open_mensa.setAttribute(
            "xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance"
        )
        open_mensa.setAttribute(
            "xsi:schemaLocation",
            "http://openmensa.org/open-mensa-v2 "
            + "http://openmensa.org/open-mensa-v2.xsd",
        )

        version = self.__create_version_node(doc)
        open_mensa.appendChild(version)
        canteen = self.canteen.xml_element(doc)
        open_mensa.appendChild(canteen)
        return open_mensa
