import src.application.Domain.Match as Match
import src.util.util as util
import src.util.SQLLite as SQLLite

import logging

class League(object):
    def __init__(self, id):
        self.id = id

    def __str__(self):
        to_string = "League "
        attributes = util.read_config_file("src/util/SQLLite.ini","League")
        for attribute in attributes.keys():
            try:
                to_string+=attribute+": "+str(self.__getattribute__(attribute))+", "
            except AttributeError:
                logging.debug("League :: AttributeError ["+attribute+"]")
        return to_string

    def get_seasons(self):
        seasons = []
        query = "SELECT distinct(season) FROM Match WHERE league_id='"+str(self.id)+"'"
        for sqllite_row in SQLLite.get_connection().execute_query(query):
            seasons.append(sqllite_row[0])
        return seasons

    def get_matches(self,season=None):
        return Match.read_matches_by_league(self.id, season)



def read_all():
    league_list = []
    for p in SQLLite.read_all("League"):
        league = League(p["id"])
        for attribute, value in p.items():
            league.__setattr__(attribute, value)
        league_list.append(league)
    return league_list

def read_by_country(country_id):
    sqllite_row = SQLLite.get_connection().select("League", **{"country_id": country_id})[0]
    league = League(sqllite_row["id"])
    for attribute, value in sqllite_row.items():
        league.__setattr__(attribute, value)

    return league
