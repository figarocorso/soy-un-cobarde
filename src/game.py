import pytz

import unittest
from datetime import datetime


SCHEDULE_FORMAT = "%d/%m/%Y %H:%M"


class Game:
    def __init__(self, game_source):
        self.hosting = None
        self.visiting = None
        self.schedule = None
        self.channel = None

        self.game_source = game_source

        if isinstance(game_source, dict):
            self.get_info_from_dict()
        else:
            self.get_info_from_li()

    def __str__(self):
        return str(self.info)

    def __bool__(self):
        return bool(self.hosting is not None and self.visiting is not None)

    @property
    def info(self):
        return {
            "hosting": self.hosting,
            "visiting": self.visiting,
            "iso": self.iso_schedule,
            "channel": self.channel if self.channel else "",
        }

    @property
    def iso_schedule(self):
        return self.schedule.isoformat()

    def get_info_from_dict(self):
        self.hosting = self.game_source.get("hosting", "")
        self.visiting = self.game_source.get("visiting", "")
        self.schedule = datetime.fromisoformat(self.game_source.get("iso", ""))

    def get_info_from_li(self):
        self.add_schedule()
        self.add_teams()
        self.add_channel()

    def add_schedule(self):
        day_month = self.game_source.find("span", {"class": "week"}).contents[0]
        time = self.game_source.find("span", {"class": "hour"}).contents[0].replace("h", "")
        year = self._get_game_year_from_li_info(day_month)

        dt = datetime.strptime(f"{day_month}/{year} {time}", SCHEDULE_FORMAT)
        self.schedule = pytz.timezone('Europe/Madrid').localize(dt)

    def _get_game_year_from_li_info(self, day_month):
        today = datetime.today()
        day, month = day_month.split("/")
        return today.year + 1 if month == "01" and today.month == 12 else today.year

    def add_teams(self):
        teams = self.game_source.find("div", {"class": "title-team"}).find_all(attrs={"itemprop": "name"})
        if teams:
            self.hosting = teams[0].contents[0]
            self.visiting = teams[1].contents[0]

    def add_channel(self):
        channel_url = self.game_source.find("ul", {"class": "channels"}).find("a").get("href", "")

        self.channel = ""
        if "m-plus-deportes" in channel_url:
            self.channel = "Movistar Plus Deportes"
        elif "m-plus-vamos" in channel_url:
            self.channel = "Movistar Plus Vamos"
        elif "m-plus-0" in channel_url:
            self.channel = "Movistar Plus 0"


class GameTest(unittest.TestCase):
    def test_foo(self):
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
