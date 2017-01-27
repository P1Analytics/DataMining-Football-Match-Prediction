import os

from src.application.data.CSV_Reader import  CSV_Reader
from src.util import util

class MatchesResultReader(object):
    def __init__(self, league):
        self.league_path = util.get_project_directory()+"data/matches/"+league
        self.league = league


    def read_matches(self, team1, team2, order=True):
        list_of_matches = []        # list of pairs < DATE , RESULT >
        for file_name in os.listdir(self.league_path):
            if file_name == ".DS_Store":
                continue
            csv_reader = CSV_Reader("data/matches/"+self.league+"/"+file_name)
            matches = csv_reader.get_elements(header=True)
            for match in matches:
                if (match["HomeTeam"] == team1 and match["AwayTeam"]==team2) or (match["HomeTeam"] == team2 and match["AwayTeam"]==team1):
                    result = 1
                    if(int(match["FTHG"])>int(match["FTAG"])):
                        if match["HomeTeam"] == team1:
                            result = 3
                        else:
                            result = 0
                    elif(int(match["FTHG"])<int(match["FTAG"])):
                        if match["HomeTeam"] == team1:
                            result = 0
                        else:
                            result = 3
                    list_of_matches.append((match["Date"], result))
        return list_of_matches

