import src.application.Domain.Country as Countries
import src.application.Domain.Player as Players
import src.application.Domain.Team as Team
import src.application.Domain.Match as Match
import src.application.Domain.League as League
import src.util.Cache as Cache

print(Team.read_by_name('Crotone')[0])

match = Match.read_by_match_api_id(2252423)
print(match)

for match in Team.read_by_name("Manchester City")[0].get_matches(season="2016/2017", ordered=True):
    print(match.get_home_team(),match.get_away_team())
    print(match.match_api_id)
    print(not match or not match.are_teams_linedup() or not match.are_incidents_managed() or not match.get_home_team() or not match.get_away_team())
    print(not match)
    print(not match.are_teams_linedup())
    print(not match.are_incidents_managed())
    print(not match.get_home_team())
    print(not match.get_away_team())
    print("FIN", match.is_finished())
    print()


match = Match.read_by_match_api_id(2319806)
print(match)

#print(match)


for l in League.read_all():
    print(l)

print(League.read_by_name('Belgium Jupiler League|Belgian Jupiler Pro League')[0].get_matches(season='2016/2017'))