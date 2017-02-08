import requests
from bs4 import BeautifulSoup

import src.application.Domain.League as League
import src.util.util as util


class CrawlerTeam(object):
    def __init__(self, team, team_link, host_url = "http://sofifa.com"):
        self.host_url = host_url
        self.team = team
        self.team_link = team_link

    def look_for_players(self, force_parsing=True):
        current_players = self.team.get_current_players()
        players_found = {}
        if len(current_players) == 0 or force_parsing:
            page = requests.get(self.team_link).text
            soup = BeautifulSoup(page, "html.parser")

            table = soup.find('table', {"class": "table table-striped table-hover no-footer"})
            for tr in table.find_all("tr"):
                a = tr.find("a")
                if a:
                    team_name = str(a.string).strip()
                    link = self.host_url + a["href"]
                    players_found[link] = team_name
        return players_found


    def look_for_team_attributes(self, time_passed = 21, force_parsing=True):
        last_team_attributes = self.team.get_last_team_attributes()
        attributes_found = {}
        if not last_team_attributes or util.compare_time_to_now(last_team_attributes.date, time_passed) or force_parsing:
            page = requests.get(self.team_link).text
            soup = BeautifulSoup(page, "html.parser")

            div = soup.find('div', {"class": "card mb-20"})
            i = 0
            for li in div.find_all("li"):
                value_str = str(li.span.string)
                name = get_group_label(i)+get_db_format(str(li.get_text())[0:-len(value_str)])

                # value --> quantita
                # value_class --> label

                if value_str[0].isdigit():
                    value = value_str[0:value_str.index("(")]
                    value_class = value_str[value_str.index("(")+1:-1]

                    attributes_found[name] = value
                    attributes_found[name+"Class"] = value_class
                else:
                    value_class = value_str
                    attributes_found[name + "Class"] = value_class

                i=i+1
        return attributes_found


def get_group_label(i):
    if i//4 == 0:
        return "buildUpPlay"
    elif i//4==1:
        return "chanceCreation"
    elif i//4==2:
        return "defence"

def get_db_format(text):
    db_text = ""
    for t in text.split(" "):
        db_text += t.title()
    return db_text