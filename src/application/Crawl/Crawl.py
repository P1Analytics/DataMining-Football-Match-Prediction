import _thread
import time
import os, sys

import src.application.Crawl.enetscores.Crawler as CrawlerMatches
import src.application.Crawl.sofifa.Crawler as CrawlerPlayers
import src.application.Crawl.football_data.Crawler as CrawlerBetOdds

import src.util.util as util

def flush_output(log_file):
    while True:
        log_file.flush()
        time.sleep(1)

def start_threads():
    try:
        log_file = open(util.get_project_directory()+"/data/log/crawl_log.txt", "w")
        sys.stdout = log_file

        _thread.start_new_thread(flush_output, (log_file,))

        # crawl matches
        starting_date = util.get_date(-7)
        stop_when = 10
        CrawlerMatches.start_crawling(5, stop_when, starting_date)

        # crawl bet-odds
        CrawlerBetOdds.start_crawling()

        # crawl players
        CrawlerPlayers.start_crawling()
    except KeyboardInterrupt:
        pass

from multiprocessing import Process

def run_init_crawl():
    p = Process(target=start_threads, args=())
    print("> Init crawling: started")
    p.start()




