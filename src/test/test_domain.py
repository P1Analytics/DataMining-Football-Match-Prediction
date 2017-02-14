import src.application.Domain.Country as Countries
import src.application.Domain.Player as Players
import src.application.Domain.Team as Team
import src.application.Domain.Match as Match
import src.util.Cache as Cache

print(Team.read_by_name('Crotone')[0])

for match in Match.read_matches_by_team(9884):
    print(not match or not match.are_teams_linedup() or not match.are_incidents_managed() or not match.get_home_team() or not match.get_away_team())
    print(not match)
    print(not match.are_teams_linedup())
    print(not match.are_incidents_managed())
    print(not match.get_home_team())
    print(not match.get_away_team())
    print()