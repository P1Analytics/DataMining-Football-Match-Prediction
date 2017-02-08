from src.application.Crawl.Crawler import Crawler
from src.application.Crawl.CrawlerLeague import CrawlerLeague
from src.application.Crawl.CrawlerTeam import CrawlerTeam
import src.application.Domain.League as League
import src.application.Domain.Team as Team

def test():
    c = Crawler()

    # looking for league
    link_league_found = c.look_for_leagues()
    c.find_thesaurus_legues(link_league_found.values())
    c.find_new_league_to_manage(link_league_found.values())

    for league_link, league_name in link_league_found.items():
        league = League.read_by_name(league_name)
        if league:
            cl = CrawlerLeague(league)

            # looking for teams
            link_teams_found = cl.look_for_teams(league_link)
            cl.find_new_team_to_manage(link_teams_found.values())

            team_not_found_in_db = []
            for team_link, team_name in link_teams_found.items():
                team = Team.read_by_name(team_name)
                if team:
                    ct = CrawlerTeam(team, team_link)

                    #print("looking for player of",team_link, team_name)

                    # looking for player
                    link_players_found = ct.look_for_players()

                    # looking for build up play
                    attributes_found = ct.look_for_team_attributes()
                else:
                    # team non found in the Database, an human check is necessary
                    team_not_found_in_db.append(team_name)

            print(league_name, "team not found", team_not_found_in_db)


test()