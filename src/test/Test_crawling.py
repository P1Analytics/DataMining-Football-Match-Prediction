import src.application.Crawl.enetscores.Crawler as Crawler
import src.application.Domain.Country as Country
import src.application.Domain.Team as Team
import src.application.Domain.Match as Match
import src.util.util as util

util.init_logger()
Crawler.start_crawling()

# live score!!!
# today matches : http://json.mx-api.enetscores.com/live_data/livescore/1/0/
# teams : http://football-data.mx-api.enetscores.com/page/mx/team/9875
# events : http://json.mx-api.enetscores.com/live_data/event/2446606/0
# get_matches_from data: http://football-data.mx-api.enetscores.com/page/xhr/sport_events/1%2F2017-02-08%2Fbasic_h2h%2F0%2F0/

# incidents http://football-data.mx-api.enetscores.com/page/xhr/event_gamecenter/2320039%2Fstandalone_incidents/bb96e0c5b313e50f204f447ed951d259
# livestats http://football-data.mx-api.enetscores.com/page/xhr/event_gamecenter/2320039%2Fstandalone_livestats/53b4751af7132b81b764afff7da454bb
# formation http://football-data.mx-api.enetscores.com/page/xhr/event_gamecenter/2320039%2Fv2_lineup/5d2ccf5c83dda7bf83f2820c046c460b

napoli = Team.read_by_name("Chaves", like=True)
#napoli = Team.read_by_team_fifa_api_id(111821)
print(napoli)

match_api_id = "483129"
print(Match.read_by_match_api_id(match_api_id))



