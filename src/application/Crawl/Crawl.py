import _thread
import time
import sys
import src.application.Crawl.enetscores.Crawler as CrawlerMatches
import src.application.Crawl.sofifa.Crawler as CrawlerPlayers
import src.application.Crawl.football_data.Crawler as CrawlerBetOdds
import src.util.util as util
from multiprocessing import Process


def flush_output(log_file):
    """
    Flush file every second
    :param log_file:
    :return:
    """
    if log_file:
        while True:
            log_file.flush()
            time.sleep(1)


def start_threads():
    """
    function called in when the new process is created
    :return:
    """
    try:
        log_file = open(util.get_project_directory()+"data/log/crawl_log.txt", "w")
        # turn the stdout into the new log file
        sys.stdout = log_file

        _thread.start_new_thread(flush_output, (log_file,))

        # crawl matches
        starting_date = util.get_date(-7)
        stop_when = 10
        CrawlerMatches.start_crawling(True, stop_when, starting_date)

        # crawl bet-odds
        CrawlerBetOdds.start_crawling()

        # crawl players
        CrawlerPlayers.start_crawling()
    except KeyboardInterrupt:
        pass


def run_init_crawl():
    p = Process(target=start_threads, args=())
    print("> Init crawling: started")
    p.start()
