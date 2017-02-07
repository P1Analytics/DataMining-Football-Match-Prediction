from src.application.Crawl.Crawler import Crawler
import src.application.Domain.League as League

def test():
    c = Crawler()
    link_league_found = c.look_for_leagues()
    c.find_thesaurus_legues(link_league_found.values())
    c.find_new_league_to_manage(link_league_found.values())

    from src.application.Crawl.CrawlerLeague import CrawlerLeague
    for link, league_name in link_league_found.items():
        league = League.read_by_name(league_name)
        if league:
            cl = CrawlerLeague(league)
            link_teams_found = cl.look_for_teams(link)
            cl.find_new_team_to_manage(link_teams_found.values())

test()