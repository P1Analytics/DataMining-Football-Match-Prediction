import calendar
import logging
import requests

from bs4 import BeautifulSoup

import src.application.Domain.Player as Player

log = logging.getLogger(__name__)
class CrawlerPlayer(object):
    def __init__(self, player, player_link, host_url = "http://sofifa.com"):
        self.host_url = host_url
        self.player = player
        self.player_link = player_link

        page = ""
        retry = 1
        succeed_request = False
        while not succeed_request or retry > 5:
            try:
                page = requests.get(self.player_link).text
                succeed_request = True
            except:
                log.debug("Error during the request of the page ["+player_link+"]. Retry #"+str(retry))
                retry += 1
        if retry > 5:
            log.debug("Impossible to retrieve page ["+player_link+"]")
            raise BaseException

        self.soup = BeautifulSoup(page, "html.parser")

    def start_crawling(self):
        if not self.player:
            # looking for player name and fifa_api_id
            player_name, player_fifa_api_id, birthday, height, weight = self.look_for_base_data()

            # try to read the player by name
            plabyers_by_name = Player.read_by_name(player_name, like=True)
            if len(plabyers_by_name)==1:
                print("Found a player without fifa api id but with name", plabyers_by_name[0])
            self.player = Player.write_new_player(player_name, player_fifa_api_id, birthday, height, weight)
            print("Player inserted:",self.player.player_name)

        # looking for player atrtbiutes
        try:
            attributes_found = self.look_for_player_attributes()
            self.player.save_player_attributes(attributes_found)
        except IndexError:
            log.debug("Error during parsing of ["+self.player_link+"]")
            for i, ul in enumerate(self.soup.find_all('ul', {"class": "pl"})):
                print("*****", i, self.player_link, "*****")
                print(ul.prettify())
            exit(-1)

    def look_for_player_attributes(self):
        log.debug("Start looking for player attributes ["+self.player_link+"]")
        attributes_found = {}

        # OVA, POT (Overall rating, Potential)
        div_stats = self.soup.find('div', {"class": "stats"})
        attributes_found["overall_rating"]=str(div_stats.find_all("td")[0].span.string)
        attributes_found["potential"] = str(div_stats.find_all("td")[1].span.string)

        # preferred_foot, attacking_work_rate, defensive_work_rate
        div_stats = self.soup.find('div', {"class": "teams"})
        attributes_found["preferred_foot"] = str(div_stats.find_all("li")[0].get_text()[16:])
        attributes_found["attacking_work_rate"] = str(div_stats.find_all("li")[4].get_text()[11:]).split("/")[0].strip()
        attributes_found["defensive_work_rate"] = str(div_stats.find_all("li")[4].get_text()[11:]).split("/")[1].strip()

        ul_pl = self.soup.find_all('ul', {"class": "pl"})
        index_statistics = 2
        # attacking
        try:
            li_ul_attacking = ul_pl[index_statistics].find_all('li')
            attributes_found["crossing"] = li_ul_attacking[0].span.get_text()
        except AttributeError:
            # this player also has Country information
            index_statistics = 3

        li_ul_attacking = ul_pl[index_statistics].find_all('li')
        attributes_found["crossing"] = li_ul_attacking[0].span.get_text()
        attributes_found["finishing"] = li_ul_attacking[1].span.get_text()
        attributes_found["heading_accuracy"] = li_ul_attacking[2].span.get_text()
        attributes_found["short_passing"] = li_ul_attacking[3].span.get_text()
        attributes_found["volleys"] = li_ul_attacking[4].span.get_text()


        # skill
        index_statistics += 1
        li_ul_skill = ul_pl[index_statistics].find_all('li')
        attributes_found["dribbling"] = li_ul_skill[0].span.get_text()
        attributes_found["curve"] = li_ul_skill[1].span.get_text()
        attributes_found["free_kick_accuracy"] = li_ul_skill[2].span.get_text()
        attributes_found["long_passing"] = li_ul_skill[3].span.get_text()
        attributes_found["ball_control"] = li_ul_skill[4].span.get_text()


        # Movement
        index_statistics += 1
        li_ul_movement = ul_pl[index_statistics].find_all('li')
        attributes_found["acceleration"] = li_ul_movement[0].span.get_text()
        attributes_found["sprint_speed"] = li_ul_movement[1].span.get_text()
        attributes_found["agility"] = li_ul_movement[2].span.get_text()
        attributes_found["reactions"] = li_ul_movement[3].span.get_text()
        attributes_found["balance"] = li_ul_movement[4].span.get_text()


        # Power
        index_statistics += 1
        li_ul_power = ul_pl[index_statistics].find_all('li')
        attributes_found["shot_power"] = li_ul_power[0].span.get_text()
        attributes_found["jumping"] = li_ul_power[1].span.get_text()
        attributes_found["stamina"] = li_ul_power[2].span.get_text()
        attributes_found["strength"] = li_ul_power[3].span.get_text()
        attributes_found["long_shots"] = li_ul_power[4].span.get_text()

        # Mentality
        index_statistics += 1
        li_ul_mentality = ul_pl[index_statistics].find_all('li')
        attributes_found["aggression"] = li_ul_mentality[0].span.get_text()
        attributes_found["interceptions"] = li_ul_mentality[1].span.get_text()
        attributes_found["positioning"] = li_ul_mentality[2].span.get_text()
        attributes_found["vision"] = li_ul_mentality[3].span.get_text()
        attributes_found["penalties"] = li_ul_mentality[4].span.get_text()
        #attributes_found["Composure"] = li_ul_mentality[5].span.get_text()         TODO add this field in the DB


        # Defending
        index_statistics += 1
        li_ul_defending = ul_pl[index_statistics].find_all('li')
        attributes_found["marking"] = li_ul_defending[0].span.get_text()
        attributes_found["standing_tackle"] = li_ul_defending[1].span.get_text()
        attributes_found["sliding_tackle"] = li_ul_defending[2].span.get_text()


        # Goalkeeping
        index_statistics += 1
        li_ul_goalkeeping = ul_pl[index_statistics].find_all('li')
        attributes_found["gk_diving"] = li_ul_goalkeeping[0].span.get_text()
        attributes_found["gk_handling"] = li_ul_goalkeeping[1].span.get_text()
        attributes_found["gk_kicking"] = li_ul_goalkeeping[2].span.get_text()
        attributes_found["gk_positioning"] = li_ul_goalkeeping[3].span.get_text()
        attributes_found["gk_reflexes"] = li_ul_goalkeeping[4].span.get_text()

        return attributes_found

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

        height = meta_text[meta_text.index(")"):].split(" ")[1]
        height = get_db_height(height)

        weight = meta_text[meta_text.index(")"):].split(" ")[2][:-1]
        weight = get_db_weight(weight)

        return player_long_name, int(player_fifa_api_id), birthday+" 00:00:00", height, weight


def get_db_birthday_date(birthday_text):
    month_str = birthday_text.split(" ")[0]

    day = int(birthday_text.split(" ")[1][:-1])
    month = {v: k for k,v in enumerate(calendar.month_abbr)}[month_str]

    year = birthday_text.split(" ")[2]
    return year+"-"+'{0:02d}'.format(month)+"-"+'{0:02d}'.format(day)


def get_db_height(height_text):
    height = -1
    if height_text.endswith("cm"):
        height = float(height_text[:-2])
    elif height_text.endswith("\""):
        # convert "piedi" --> "cm"
        height = float(height_text[0])*30.48
        height += float(height_text[-1])*2.54

    return height

def get_db_weight(weight_text):
    weight = -1
    if weight_text.endswith("kg"):
        # convert kg to lbs
        weight = int(float(weight_text[:-2])*2.20462)
    elif weight_text.endswith("lbs"):
        weight = weight_text

    return weight




