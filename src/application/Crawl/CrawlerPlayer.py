import requests
from bs4 import BeautifulSoup

import calendar


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
            player_name, player_fifa_api_id, birthday, height, weight = self.look_for_base_data()





    def look_for_base_data(self):
        div = self.soup.find('div', {"class": "info"})

        # name and fifa api id
        h1 = div.h1
        data_string = str(h1.string)
        player_long_name = data_string[0:data_string.index("(")].strip()
        player_fifa_api_id = data_string[data_string.index("(") + 1:-1].split(" ")[1]

        # birthday height and weight
        meta_text = str(div.find('div', {"class":"meta"}).get_text())
        row_birthday = meta_text[meta_text.index("(")+1:meta_text.index(")")]
        birthday = get_db_birthday_date(row_birthday)

        # TODO weight and height


        return player_long_name, int(player_fifa_api_id), birthday+" 00:00:00", 0, 0


def get_db_birthday_date(birthday_text):
    month_str = birthday_text.split(" ")[0]

    day = int(birthday_text.split(" ")[1][:-1])
    month = {v: k for k,v in enumerate(calendar.month_abbr)}[month_str]

    year = birthday_text.split(" ")[2]
    return year+"-"+'{0:02d}'.format(month)+"-"+'{0:02d}'.format(day)



