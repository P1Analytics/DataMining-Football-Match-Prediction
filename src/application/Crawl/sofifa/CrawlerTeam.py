import logging
import requests
import src.util.util as util
import src.application.Domain.Team as Team
import src.application.Domain.Player as Player
from bs4 import BeautifulSoup
from src.application.Crawl.sofifa.CrawlerPlayer import CrawlerPlayer

log = logging.getLogger(__name__)


class CrawlerTeam(object):
    def __init__(self, team, team_link, host_url="http://sofifa.com", day_passed=2, force_parsing=False):
        self.host_url = host_url
        self.team = team
        self.team_link = team_link

        page = requests.get(self.team_link).text
        self.soup = BeautifulSoup(page, "html.parser")

        self.day_passed = day_passed
        self.force_parsing = force_parsing
        log.debug("Crawler Instantiated ["+self.team_link+", "+str(self.day_passed)+", "+str(self.force_parsing)+"]")

    def look_for_players(self):
        """
        start looking for player of this team
        :return:
        """
        log.debug("Start looking for players [" + self.team_link + "]")

        players_found = {}
        table = self.soup.find('table', {"class": "table table-striped table-hover no-footer"})
        for tr in table.find_all("tr"):
            a = tr.find("a")
            if a:
                # tag a container of the name player found
                player_name = str(a.string).strip()
                link = self.host_url + a["href"]
                players_found[link] = player_name

        return players_found

    def look_for_team_attributes(self, day_passed=21, force_parsing=False):
        """
        Gather team attributes
        :param day_passed:
        :param force_parsing:
        :return:
        """
        last_team_attributes = self.team.get_last_team_attributes()
        attributes_found = {}

        # crawl team attributes if and only if one of this condition hold:
        #   1) no team attributes about this team are in the DB
        #   2) team attributes in the DB are old
        #   3) force the crawl
        if not last_team_attributes or util.compare_time_to_now(last_team_attributes.date, day_passed) or force_parsing:
            div = self.soup.find('div', {"class": "card mb-20"})
            i = 0
            for li in div.find_all("li"):
                value_str = str(li.span.string)
                name = get_group_label(i)+get_db_format(str(li.get_text())[0:-len(value_str)])

                # Each attribute has a quantity, which corresponds to a label
                #   value --> quantity
                #   value_class --> label

                if value_str[0].isdigit():
                    value = value_str[0:value_str.index("(")]
                    value_class = value_str[value_str.index("(")+1:-1]

                    attributes_found[name] = value
                    attributes_found[name+"Class"] = value_class
                else:
                    value_class = value_str
                    attributes_found[name + "Class"] = value_class

                i += 1
        return attributes_found

    def look_for_base_data(self):
        """
        Looking for the most important data of a team
        :return:
        """
        h1 = self.soup.find('div', {"class": "info"}).h1
        data_string = str(h1.string)
        team_long_name = data_string[0: data_string.index("(")].strip()
        team_fifa_api_id = data_string[data_string.index("(") + 1: -1].split(" ")[1]
        return team_long_name, int(team_fifa_api_id)

    def start_crawling(self):
        """
        Start crawling this team
        :return:
        """
        if util.is_None(self.team) or (not util.is_None(self.team) and util.is_None(self.team.team_fifa_api_id)):
            # If one of the follow:
            # 1) team not stored in the DB
            # 2) Team fifa api id not stored in the DB
            # --> looking for name and fifa_api_id
            team_long_name, team_fifa_api_id = self.look_for_base_data()

            if util.is_None(self.team):
                # team not present in the DB
                self.team = Team.write_new_team(team_long_name, team_fifa_api_id)
            else:
                # team present in the DB, but without set the team_fifa_api_id
                self.team.team_fifa_api_id = team_fifa_api_id
                self.team = Team.update(self.team)

        # looking for players belonging this team
        link_players_found = self.look_for_players()
        for player_link, player_name in link_players_found.items():
            player_fifa_api_id = player_link[25:]
            player = Player.read_by_fifa_api_id(player_fifa_api_id)

            # crawl the player if and only if on of the following happens:
            # 1) PLAYER DOES NOT EXIST IN THE DB
            # 2) PLAYER ATTRIBUTES DO NOT EXIST IN THE DB
            # 3) PLAYER ATTRIBUTES IN THE DB ARE OLD
            # 4) FORCE PARSING OF PLAYER ATTRIBUTES
            if \
                    not player \
                    or not player.get_last_player_attributes() \
                    or util.compare_time_to_now(player.get_last_player_attributes().date, self.day_passed) \
                    or self.force_parsing:
                log.debug("Player to crawl ["+player_link+", "+player_name+"]")
                cp = CrawlerPlayer(player, player_link)
                cp.start_crawling()

        # looking for build up play
        attributes_found = self.look_for_team_attributes()
        if len(attributes_found) > 0:
            self.team.save_team_attributes(attributes_found)


def get_group_label(i):
    """
    every 4 property there is a different label
    :param i:
    :return:
    """
    if i//4 == 0:
        return "buildUpPlay"
    elif i//4 == 1:
        return "chanceCreation"
    elif i//4 == 2:
        return "defence"


def get_db_format(text):
    """
    return the string without spaces, and upper every initial character
    :param text:
    :return:
    """
    db_text = ""
    for t in text.split(" "):
        db_text += t.title()
    return db_text
