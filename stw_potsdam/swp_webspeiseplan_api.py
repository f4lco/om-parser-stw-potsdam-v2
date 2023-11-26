import logging
import urllib.request
import re
import time
import json


class SWP_Webspeiseplan_API:
    def __init__(self):
        logging.basicConfig()
        self.logger = logging.getLogger(__name__)
        self.url_base = "https://swp.webspeiseplan.de"
        self.__parse_token()
        params = {
            "token": self.proxy_token,
            "model": "outlet",
            "location": "",
            "languagetype": "",
            "_": int(time.time() * 1000),
        }

        self.outlets = {outlet["name"]: outlet for outlet in self.__parse_model(params)}
        self.menus = {}
        self.meal_categories = {}
        for outlet in self.outlets.values():
            params["model"] = "menu"
            params["location"] = outlet["standortID"]
            params["languagetype"] = 2
            params["_"] = int(time.time() * 1000)
            menu = self.__parse_model(params)
            self.menus[outlet["name"]] = menu

            params["model"] = "mealCategory"
            params["_"] = int(time.time() * 1000)
            categories = self.__parse_model(params)
            id2cat = {item["gerichtkategorieID"]: item for item in categories}
            self.meal_categories[outlet["name"]] = id2cat

    def __parse_token(self):
        req = urllib.request.Request(self.url_base)
        with urllib.request.urlopen(req) as resp:
            txt = resp.read().decode("utf-8")
        match = re.findall(r"/main.[0-9a-f]+.js", txt)[0]
        self.logger.debug(f"__parse_token: downloading script {match}")
        req = urllib.request.Request(f"{self.url_base}{match}")
        with urllib.request.urlopen(req) as resp:
            txt = resp.read().decode("utf-8")
        self.proxy_token = re.findall(r"PROXY_TOKEN:\"([0-9a-f]+)\"", txt)[0]
        self.logger.debug(f"__parse_token: PROXY_TOKEN {self.proxy_token}")

    def __spoof_req_headers(req: urllib.request.Request):
        req.add_header("Accept", "application/json, text/javascript, */*; q=0.01")
        req.add_header("Accept-Language", "en-US,en;q=0.9")
        req.add_header("Connection", "keep-alive")
        req.add_header("Host", "swp.webspeiseplan.de")
        req.add_header("Referer", "https://swp.webspeiseplan.de/InitialConfig")
        req.add_header(
            "Sec-Ch-Ua",
            '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        )
        req.add_header("Sec-Ch-Ua-Mobile", "?0")
        req.add_header("Sec-Ch-Ua-Platform", "Linux")
        req.add_header("Sec-Fetch-Dest", "empty")
        req.add_header("Sec-Fetch-Mode", "cors")
        req.add_header("Sec-Fetch-Site", "same-origin")
        req.add_header(
            "User-Agent",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        )
        req.add_header("X-Requested-With", "XMLHttpRequest")

    def __parse_model(self, params: dict):
        url = f"{self.url_base}/index.php?" + "&".join(
            [f"{k}={v}" for k, v in params.items()]
        )
        self.logger.debug(f"__parse_model: {url}")
        req = urllib.request.Request(url)
        SWP_Webspeiseplan_API.__spoof_req_headers(req)
        with urllib.request.urlopen(req) as resp:
            data = resp.read()
        return json.loads(data)["content"]

