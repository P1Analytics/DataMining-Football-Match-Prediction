import requests
from bs4 import BeautifulSoup

class HTTPRequest(object):
    def __init__(self,url):
        self.url = url

    def get_ranking(self,nation):
        try:
            print(self.url + "/ranking/" + nation)
            page = requests.get(self.url + "/ranking/" + nation).text
            soup = BeautifulSoup(page,"xml")
            team_titles = soup.find_all("td",{"class":"club text-left"})
            team_ranks = soup.find_all("td",{"class":"rank"})
            team_ranks = [x.text for x in team_ranks]
            team_ranks = team_ranks[1::2]
            team_ranking = []
            if len(team_ranks) == len(team_titles):
                for x,y in zip(team_titles,team_ranks):
                    my_str = x.text
                    team_title = str(my_str).replace(nation.title(),"")
                    team_rank = y
                    team_ranking.append((team_title,team_rank))
                return 0,team_ranking
            else:
                return -1,[]

        except:
            print(requests.HTTPError)
            return -1,[]


http = HTTPRequest("http://footballdatabase.com")
index,my_list = http.get_ranking("italy")
for x in my_list:
    print(x)

