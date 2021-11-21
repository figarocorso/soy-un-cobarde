import pathlib
import json

import requests
from bs4 import BeautifulSoup

from game import Game

URL = "https://www.movistarplus.es/nba/horarios"


FILE = f"{pathlib.Path(__file__).parent.absolute()}/../schedule.json"


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
