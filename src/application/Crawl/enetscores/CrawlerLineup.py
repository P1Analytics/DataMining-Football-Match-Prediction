import logging
import requests

from bs4 import BeautifulSoup

log = logging.getLogger(__name__)

class CrawlerLineup(object):
    def __init__(self, match, event):
        self.match = match
        self.event = event

        self.match_linedup_link = "http://football-data.mx-api.enetscores.com/page/xhr/event_gamecenter/"+event+"%2Fv2_lineup/"
        page = requests.get(self.match_linedup_link).text
        self.soup = BeautifulSoup(page, "html.parser")

        log.debug("Match linedups event [" + event + "] got at link [" + self.match_linedup_link + "]")

    def get_lineups(self, match_attrbitues):
        print(self.soup.prettify())
