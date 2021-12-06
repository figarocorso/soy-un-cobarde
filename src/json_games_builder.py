from datetime import datetime, timedelta
import pathlib
import json

import pytz
import requests
from bs4 import BeautifulSoup

from game import Game

PAST_GAMES = 6

URL = "https://www.movistarplus.es/nba/horarios"

HISTORICAL_GAMES_FILE = f"{pathlib.Path(__file__).parent.absolute()}/../games/historical.json"
RECENT_GAMES_FILE = f"{pathlib.Path(__file__).parent.absolute()}/../games/schedule.json"


class JsonGamesBuilder:
    def __init__(self):
        self.now = pytz.timezone('Europe/Madrid').localize(datetime.now())
        self.games = []
        self.load_games_file()
        self.html = ""

    def load_games_file(self):
        with open(HISTORICAL_GAMES_FILE, "r") as games_file:
            json_games = json.load(games_file)

        for json_game in json_games:
            game = Game(json_game)
            if game.schedule > self.now:
                break
            self.games.append(game)

    def save_hitorical_games_file(self):
        with open(HISTORICAL_GAMES_FILE, "w") as games_file:
            json.dump([game.info for game in self.games], games_file, indent=2)

    def save_recent_games_file(self):
        recent_games = [game for game in self.games
                        if game.schedule >= (self.now - timedelta(days=PAST_GAMES))]

        with open(RECENT_GAMES_FILE, "w") as games_file:
            json.dump([game.info for game in recent_games], games_file, indent=2)

    def retrieve_html_page(self):
        response = requests.get(URL)
        response.raise_for_status()
        self.html = response.content

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
            if game.schedule == new_game.schedule:
                return
        self.games.append(new_game)
