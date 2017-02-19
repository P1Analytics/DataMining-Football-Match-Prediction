import src.application.Domain.Country as Countries
import src.application.Domain.Player as Players
import src.application.Domain.Team as Team
import src.application.Domain.Match as Match
import src.application.Domain.MatchEvent as Match_Event
import src.application.Domain.League as League
import src.util.Cache as Cache
import src.util.SQLLite as SQLLite

team = Team.read_by_name('inter', like=True)[0]
print(team)

eder = Players.read_by_name('Eder Citadin Martins')[0]
print(eder)

