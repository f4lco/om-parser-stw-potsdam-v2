from xml.dom import minidom
from dataclasses import dataclass


@dataclass
class MealXML:
    """Represents the meal tag in openMensaFeedv2."""

    def __init__(self, name: str, price: dict[str, float], note: str = None):
        """Init MealXML object.

        Args:
            name (str): name of the meal
            note (str): additional information
            price (dict[str, float]): prices for student, employee and other
        """
        self.name = name
        self.note = note
        self.price = price

    def xml_element(self, doc: minidom.Document):
        """Return the xml tag.

        Args:
            doc (minidom.Document): Working XML documnet.
        """
        meal = doc.createElement("meal")
        name = doc.createElement("name")
        txt_node = doc.createTextNode(self.name)
        name.appendChild(txt_node)
        meal.appendChild(name)
        if self.note is not None:
            note = doc.createElement("note")
            txt_node = doc.createTextNode(self.note)
            note.appendChild(txt_node)
            meal.appendChild(note)

        for key, val in self.price.items():
            if key not in ("student", "employee", "other"):
                continue
            price = doc.createElement("price")
            price.setAttribute("role", key)
            txt_node = doc.createTextNode(f"{val:.2f}")
            price.appendChild(txt_node)
            meal.appendChild(price)
        return meal
