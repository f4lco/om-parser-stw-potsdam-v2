import logging
import urllib.request
import re
import time
import json


class SWPWebspeiseplanAPI:
    """This class is used download content from SWP_Webspeiseplan.

    Returns:
        [type]: [description]
    """

    URL_BASE = "https://swp.webspeiseplan.de"
    logger = logging.getLogger(__name__)

    def __init__(self):
        """Initialize the configuration for the web service."""
        logging.basicConfig()
        proxy_token = self.parse_token()
        self.outlets = self.parse_outlets(proxy_token)
        self.locations: dict[str, dict] = {}
        locations = {
            item["id"]: item
            for item in self.parse_location(proxy_token)
        }
        self.menus: dict[str, dict] = {}
        self.meal_categories: dict[str, dict] = {}
        for outlet in self.outlets.values():
            location = outlet["standortID"]
            menu = self.parse_menu(proxy_token, location)
            categories = self.parse_meal_category(proxy_token, location)
            id2cat = {item["gerichtkategorieID"]: item for item in categories}
            self.menus[outlet["name"]] = menu
            self.meal_categories[outlet["name"]] = id2cat
            self.locations[outlet["name"]] = locations[location]

    def __spoof_req_headers(self, req: urllib.request.Request):
        """Add headers to a request .

        Args:
            req (urllib.request.Request): [description]
        """
        req.add_header(
            "Accept", "application/json, text/javascript, */*; q=0.01"
        )
        req.add_header("Accept-Language", "en-US,en;q=0.9")
        req.add_header("Connection", "keep-alive")
        req.add_header("Host", "swp.webspeiseplan.de")
        req.add_header("Referer", "https://swp.webspeiseplan.de/InitialConfig")
        req.add_header(
            "Sec-Ch-Ua",
            '"Not/A)Brand";v="99", '
            + '"Google Chrome";v="115", '
            + '"Chromium";v="115"',
        )
        req.add_header("Sec-Ch-Ua-Mobile", "?0")
        req.add_header("Sec-Ch-Ua-Platform", "Linux")
        req.add_header("Sec-Fetch-Dest", "empty")
        req.add_header("Sec-Fetch-Mode", "cors")
        req.add_header("Sec-Fetch-Site", "same-origin")
        req.add_header(
            "User-Agent",
            "Mozilla/5.0 (X11; Linux x86_64) "
            + "AppleWebKit/537.36 (KHTML, like Gecko) "
            + "Chrome/115.0.0.0 Safari/537.36",
        )
        req.add_header("X-Requested-With", "XMLHttpRequest")

    def parse_model(self, params: dict):
        """Retrieve data from host.

        Args:
            params (dict): [description]

        Returns:
            [type]: [description]
        """
        url = f"{SWPWebspeiseplanAPI.URL_BASE}/index.php?" + "&".join(
            [f"{k}={v}" for k, v in params.items()]
        )
        SWPWebspeiseplanAPI.logger.debug("__parse_model: %s", url)
        req = urllib.request.Request(url)
        self.__spoof_req_headers(req)
        with urllib.request.urlopen(req) as resp:
            data = resp.read()
        return json.loads(data)["content"]

    def parse_token(self) -> str:
        """Get the token from the proxy server."""
        req = urllib.request.Request(SWPWebspeiseplanAPI.URL_BASE)
        with urllib.request.urlopen(req) as resp:
            txt = resp.read().decode("utf-8")
        match = re.findall(r"/main.[0-9a-f]+.js", txt)[0]
        SWPWebspeiseplanAPI.logger.debug(
            "__parse_token: downloading script %s", match
        )
        req = urllib.request.Request(f"{SWPWebspeiseplanAPI.URL_BASE}{match}")
        with urllib.request.urlopen(req) as resp:
            txt = resp.read().decode("utf-8")
        proxy_token = re.findall(r"PROXY_TOKEN:\"([0-9a-f]+)\"", txt)[0]
        SWPWebspeiseplanAPI.logger.debug(
            "__parse_token: PROXY_TOKEN %s", proxy_token
        )
        return proxy_token

    def parse_outlets(self, proxy_token: str) -> dict[str, dict]:
        """Get the outlets from the server."""
        params = {
            "token": proxy_token,
            "model": "outlet",
            "location": "",
            "languagetype": "",
            "_": int(time.time() * 1000),
        }

        outlets = {
            outlet["name"]: outlet for outlet in self.parse_model(params)
        }
        return outlets

    def parse_menu(self, proxy_token: str, location: int) -> dict:
        """Get the menu for a specific location."""
        params = {
            "token": proxy_token,
            "model": "menu",
            "location": location,
            "languagetype": 1,
            "_": int(time.time() * 1000),
        }
        menu = self.parse_model(params)
        return menu

    def parse_meal_category(
        self, proxy_token: str, location: int
    ) -> list[dict]:
        """Get the meal catrgories for a specific location."""
        params = {
            "token": proxy_token,
            "model": "mealCategory",
            "location": location,
            "languagetype": 1,
            "_": int(time.time() * 1000),
        }
        menu = self.parse_model(params)
        return menu

    def parse_location(self, proxy_token: str) -> list[dict]:
        """Get the meal catrgories for a specific location."""
        params = {
            "token": proxy_token,
            "model": "location",
            "location": "",
            "languagetype": 1,
            "_": int(time.time() * 1000),
        }
        menu = self.parse_model(params)
        return menu
