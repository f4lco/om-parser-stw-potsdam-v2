from dataclasses import dataclass
from xml.dom import minidom


@dataclass
class ScheduleXML:
    """Represents the schedule inside the feed tag in openMensaFeedv2."""

    def __init__(self, hour: str, **kwargs):
        """Init ScheduleXML object.

        Args:
            hour (str): _description_
            day_of_month (str, optional): _description_. Defaults to "*".
            day_of_week (str, optional): _description_. Defaults to "*".
            month (str, optional): _description_. Defaults to "*".
            minute (int, optional): _description_. Defaults to 0.
            retry (str, optional): _description_. Defaults to None.
        """
        self.hour = hour
        self.day_of_month = kwargs.get("day_of_month", "*")
        self.day_of_week = kwargs.get("day_of_week", "*")
        self.month = kwargs.get("month", "*")
        self.minute = kwargs.get("minute", 0)
        self.retry = kwargs.get("retry", None)

    def xml_element(self, doc: minidom.Document):
        """Return the XML representaion.

        Args:
            doc (minidom.Document):  Working XML document.

        Returns:
            _type_: _description_
        """
        schedule = doc.createElement("schedule")
        schedule.setAttribute("dayOfMonth", self.day_of_month)
        schedule.setAttribute("dayOfWeek", self.day_of_week)
        schedule.setAttribute("month", self.month)
        schedule.setAttribute("hour", self.hour)
        schedule.setAttribute("minute", str(self.minute))
        if self.retry:
            schedule.setAttribute("retry", self.retry)
        return schedule


@dataclass
class FeedXML:
    """Represents the feed tag in openMensaFeedv2."""

    name: str
    source: str
    url: str
    schedule: ScheduleXML
    priority: int = 0

    def xml_element(self, doc: minidom.Document):
        """Return the XML representaion.

        Args:
            doc (minidom.Document): Working XML document.

        Returns:
            _type_: _description_
        """
        feed = doc.createElement("feed")
        feed.setAttribute("name", self.name)
        feed.setAttribute("priority", str(self.priority))

        schedule = self.schedule.xml_element(doc)
        feed.appendChild(schedule)

        url = doc.createElement("url")
        tn = doc.createTextNode(self.url)
        url.appendChild(tn)
        feed.appendChild(url)

        source = doc.createElement("source")
        tn = doc.createTextNode(self.source)
        source.appendChild(tn)
        feed.appendChild(source)
        return feed
