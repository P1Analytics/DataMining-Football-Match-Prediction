import logging

import requests
from bs4 import BeautifulSoup

import src.application.Domain.Player as Player
import src.application.Domain.Team as Team
import src.util.util as util
from src.application.Crawl.sofifa.CrawlerPlayer import CrawlerPlayer

log = logging.getLogger(__name__)

class CrawlerTeam(object):
    def __init__(self, team, team_link, host_url = "http://sofifa.com", day_passed=2, force_parsing=False):
        self.host_url = host_url
        self.team = team
        self.team_link = team_link

        page = requests.get(self.team_link).text
        self.soup = BeautifulSoup(page, "html.parser")

        self.day_passed = day_passed
        self.force_parsing = force_parsing
        log.debug("Crawler Instantiated ["+self.team_link+", "+str(self.day_passed)+", "+str(self.force_parsing)+"]")

    def look_for_players(self):
        log.debug("Start looking for players [" + self.team_link + "]")

        players_found = {}
        table = self.soup.find('table', {"class": "table table-striped table-hover no-footer"})
        for tr in table.find_all("tr"):
            a = tr.find("a")
            if a:
                team_name = str(a.string).strip()
                link = self.host_url + a["href"]
                players_found[link] = team_name

        return players_found


    def look_for_team_attributes(self, day_passed = 21, force_parsing=False):
        last_team_attributes = self.team.get_last_team_attributes()
        attributes_found = {}
        if not last_team_attributes or util.compare_time_to_now(last_team_attributes.date, day_passed) or force_parsing:
            div = self.soup.find('div', {"class": "card mb-20"})
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


    def look_for_base_data(self):
        h1 = self.soup.find('div', {"class": "info"}).h1
        data_string = str(h1.string)
        team_long_name = data_string[0:data_string.index("(")].strip()
        team_fifa_api_id = data_string[data_string.index("(")+1:-1].split(" ")[1]
        return team_long_name, int(team_fifa_api_id)


    def start_crawling(self):
        if not self.team:
            # looking for name and fifa_api_id
            team_long_name, team_fifa_api_id = self.look_for_base_data()
            team = Team.read_by_team_fifa_api_id(team_fifa_api_id)
            if team:
                # a team with the same fifa api id has been found in the database
                print("Found a team [ " + team_long_name + " ] in the DB with the same fifa_api_id [ " + str(team_fifa_api_id) + " ]")
                exit(-1)
            self.team = Team.write_new_team(team_long_name, team_fifa_api_id)

        # looking for players belonging this team
        link_players_found = self.look_for_players()
        for player_link, player_name in link_players_found.items():
            player_fifa_api_id = player_link[25:]
            player = Player.read_by_fifa_api_id(player_fifa_api_id)

            # crawl the player if and only if on of the following happens:
            # PLAYER DOES NOT EXIST IN THE DB
            # PLAYER ATTRIBUTES DO NOT EXIST IN THE DB
            # PLAYER ATTRIBUTES IN THE DB ARE OLD
            # FORCE PARSING OF PLAYER ATTRIBUTES
            if not player or not player.get_last_player_attributes() or util.compare_time_to_now(player.get_last_player_attributes().date, self.day_passed) or self.force_parsing:
                log.debug("Player to crawl ["+player_link+", "+player_name+"]")
                cp = CrawlerPlayer(player, player_link)
                cp.start_crawling()

        # looking for build up play
        attributes_found = self.look_for_team_attributes()
        if len(attributes_found)>0:
            self.team.save_team_attributes(attributes_found)



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