import src.application.Crawl.sofifa.Crawler as C1
import src.application.Crawl.enetscores.Crawler as C2
import src.application.Domain.Country as Country
import src.application.Domain.League as League
import src.application.Domain.Team as Team
import src.application.Domain.Match as Match
import src.application.Domain.Player as Player
import src.util.util as util
import src.util.Cache as Cache

util.init_logger()
Cache.init_cache()
#C1.start_crawling()
C2.start_crawling(go_back=True)

print("stop")
