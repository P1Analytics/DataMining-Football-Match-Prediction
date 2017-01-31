import src.application.Domain.Country as Countries
import src.application.Domain.Player as Players
import src.application.Domain.Team as Teams
import src.util.Cache as Cache

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

print(lazio_team)
print(lazio_team.get_team_attributes())

for m in lazio_matches:
    #print(m)
    print("Homeplayer")
    print("\t")
    print(m.get_home_team().team_long_name,"vs",m.get_away_team().team_long_name)
    for attribute in dir(m):
        if attribute.startswith("home_player"):
            if not attribute.startswith("home_player_X") and not attribute.startswith("home_player_Y"):
                print("\t-",attribute,":",m.__getattribute__(attribute), Players.read_by_api_id(m.__getattribute__(attribute)).player_name)

        if attribute.startswith("home_player_X"):
            print("\t-", attribute, ":", m.__getattribute__(attribute))
        if attribute.startswith("home_player_Y"):
            print("\t-", attribute, ":", m.__getattribute__(attribute))
    print("Stage",m.stage)
    break

Cache.print_status()

