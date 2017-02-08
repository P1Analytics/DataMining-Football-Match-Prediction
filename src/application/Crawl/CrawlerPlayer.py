import requests
from bs4 import BeautifulSoup

import src.util.util as util
import src.application.Domain.Team as Team

from src.application.Domain.Player import Player


class CrawlerPlayer(object):
    def __init__(self, player, player_link, host_url = "http://sofifa.com"):
        self.host_url = host_url
        self.player = player
        self.player_link = player_link

        page = requests.get(self.player_link).text
        self.soup = BeautifulSoup(page, "html.parser")

    def start_crawling(self):
        if not self.player:
            # looking for player name and fifa_api_id
            player_name, player_fifa_api_id = self.look_for_base_data()
            print(player_name, player_fifa_api_id)


    def look_for_base_data(self):
        h1 = self.soup.find('div', {"class": "info"}).h1
        data_string = str(h1.string)
        player_long_name = data_string[0:data_string.index("(")].strip()
        player_fifa_api_id = data_string[data_string.index("(") + 1:-1].split(" ")[1]
        return player_long_name, int(player_fifa_api_id)