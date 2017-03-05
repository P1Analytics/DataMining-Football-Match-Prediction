import logging
import requests
import src.application.Domain.Team as Team
from bs4 import BeautifulSoup

log = logging.getLogger(__name__)


class CrawlerTeam(object):
    def __init__(self, team_api_id):
        self.team_api_id = team_api_id

        self.team_link = \
            "http://football-data.mx-api.enetscores.com/page/xhr/team/" + str(self.team_api_id) + "%2F0%2F1%2Fextended/"
        log.debug("Team api id to crawl ["+str(team_api_id)+"] at link ["+self.team_link+"]")

        self.soup = BeautifulSoup(requests.get(self.team_link).text, "html.parser")

    def get_team_name(self):
        """
        get names of the crawled team, both long and short
        :return:
        """
        team_long_name = str(self.soup.find_all('span', {'class': 'mx-break-micro'})[0].string).strip()
        team_short_name = str(self.soup.find_all('span', {'class': 'mx-show-micro'})[0].string).strip()

        teams = Team.read_by_name(team_long_name, like=True)
        if len(teams) == 0:
            # team not found --> store new team in the DB
            Team.write_new_team(team_long_name, None, team_api_id=self.team_api_id, team_short_name=team_short_name)
        if len(teams) == 1:
            # team found --> update its team_api_id
            teams[0].team_api_id = self.team_api_id
            teams[0].team_short_name = team_short_name
            Team.update(teams[0])
        else:
            # more than one team has been found --> manual check must be done!
            log.warning("Team with api id ["+self.team_api_id+"] and name ["
                        + team_long_name + "] at the link [" + self.team_link + "] must be matched at hand")

        return team_short_name
