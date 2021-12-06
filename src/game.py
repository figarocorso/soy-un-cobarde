import pytz

import unittest
from datetime import datetime


SCHEDULE_FORMAT = "%d/%m/%Y %H:%M"


class Game:
    def __init__(self, game_source):
        self.hosting = None
        self.visiting = None
        self.schedule = None

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

    def add_schedule(self):
        day_month = self.game_source.find("span", {"class": "week"}).contents[0]
        time = self.game_source.find("span", {"class": "hour"}).contents[0].replace("h", "")

        dt = datetime.strptime(f"{day_month}/{datetime.today().year} {time}", SCHEDULE_FORMAT)
        self.schedule = pytz.timezone('Europe/Madrid').localize(dt)

    def add_teams(self):
        teams = self.game_source.find("div", {"class": "title-team"}).find_all(attrs={"itemprop": "name"})
        if teams:
            self.hosting = teams[0].contents[0]
            self.visiting = teams[1].contents[0]


class GameTest(unittest.TestCase):
    def test_foo(self):
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
