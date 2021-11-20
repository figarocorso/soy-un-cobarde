import json
from datetime import datetime

import requests
from bs4 import BeautifulSoup

URL = "https://www.movistarplus.es/nba/horarios"
FILE = "schedule.json"


class Game:
    def __init__(self, li_tag):
        self.li_tag = li_tag
        self.when_format = "%d/%m/%Y %H:%M:%S"
        self.info = {}
        self.build_info()

    def __str__(self):
        return str(self.info)

    def __bool__(self):
        return bool(self.info.get("hosting", None) is not None
                    and self.info.get("visiting", None) is not None)

    @property
    def when(self):
        return datetime.strptime(self.info["when"], self.when_format)

    def format_when(self, dt):
        return dt.strftime(self.when_format)

    def build_info(self):
        self.add_when()
        self.add_teams()

    def add_when(self):
        day_month = self.li_tag.find("span", class_="week").contents[0]
        time = self.li_tag.find("span", class_="hour").contents[0].replace("h", "")
        data = f"{day_month}/{datetime.today().year} {time}"
        pattern = "%d/%m/%Y %H:%M"
        self.info["when"] = self.format_when(datetime.strptime(data, pattern))

    def add_teams(self):
        teams = self.li_tag.find("div", class_="title-team").find_all(attrs={"itemprop": "name"})
        if teams:
            self.info["hosting"] = teams[0].contents[0]
            self.info["visiting"] = teams[1].contents[0]


class ScheduleBuilder:
    def __init__(self):
        self.games = self.load_games_file()
        self.html = ""

    def load_games_file(self):
        with open(FILE, "r") as games_file:
            return json.load(games_file)

    def save_games_file(self):
        with open(FILE, "w") as games_file:
            json.dump(self.games, games_file, indent=2)

    def retrieve_html_page(self):
        self.html = requests.get(URL).content

    def add_html_games(self):
        if not self.html:
            self.retrieve_html_page()

        for game_li in self._get_game_lis():
            game = Game(game_li)
            if game:
                self.add_game(game)

    def _get_game_lis(self):
        soup = BeautifulSoup(self.html, "lxml")
        attrs = {"itemtype": "https://schema.org/BroadcastEvent"}
        return soup.find("div", class_="list-calendar").find_all("li", attrs=attrs)

    def add_game(self, new_game):
        for game in self.games:
            if game["when"] == new_game.info["when"]:
                return
        self.games.append(new_game.info)



def main():
    builder = ScheduleBuilder()
    builder.add_html_games()
    builder.save_games_file()


if __name__ == "__main__":
    main()
