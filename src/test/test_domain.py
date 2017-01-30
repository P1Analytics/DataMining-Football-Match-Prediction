from src.application.Domain.Country import Country
import src.application.Domain.Country as Countries
import src.application.Domain.Team as Teams

countries = Countries.read_all()
for c in countries:
    print(c.name)
    print("\t-"+c.get_league().name)

italy_league = countries[4].get_league()
italy_seasons = italy_league.get_seasons()
print(italy_seasons)

italy_matches = italy_league.get_matches("2015/2016")
lazio_team = Teams.read_by_team_api_id(8543)
lazio_matches = lazio_team.get_matches("2015/2016")

for m in lazio_matches:
    print(str(m.home_team_api_id)+" vs "+str(m.away_team_api_id))
    print(str(m.home_team_goal) + " vs " + str(m.away_team_goal))
    print(m.get_home_team())
    print(m.get_away_team())
    print(m.season)
    print()
