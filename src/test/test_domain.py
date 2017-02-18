import src.application.Domain.Country as Countries
import src.application.Domain.Player as Players
import src.application.Domain.Team as Team
import src.application.Domain.Match as Match
import src.application.Domain.League as League
import src.util.Cache as Cache
import src.util.SQLLite as SQLLite


print(Team.read_by_team_api_id(8243))
print(Team.read_by_team_api_id(8245))
#8245 8243
'''
None
Team team_long_name: Korona Kielce, id: 31925, team_short_name: KKI, team_fifa_api_id: 111083, team_api_id: 8245,
[]
'''
print(Team.read_by_name('Wisla Plock', like=True))

#SQLLite.get_connection().execute_update("DROP TABLE Bet_Event")
SQLLite.init_database()

print(SQLLite.get_connection().getTableNameDataBase())

print(SQLLite.get_connection().getColumnFromTable("Bet_Event"))