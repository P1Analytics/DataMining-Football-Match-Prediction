import sys
import os
import argparse

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import src.gui.MainGui as MainGui
import src.util.util as util
import src.util.SQLLite as SQLLite
import src.application.Crawl.Crawl as Crawl


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Score Prediction Application')
    parser.add_argument('--no-crawl', dest='do_crawl', action='store_false',
                        help='do not crawl on the start up of the application')
    parser.set_defaults(do_crawl=True)
    parser.add_argument('--no-index', dest='do_index', action='store_false',
                        help='do not index on the start up of the application')
    parser.set_defaults(do_index=True)
    args = parser.parse_args()

    util.init_logger()
    SQLLite.init_database()

    if args.do_index:
        util.indexing()

    if args.do_crawl:
        Crawl.run_init_crawl()
    try:
        MainGui.run()
    except KeyboardInterrupt:
        print("\nClosing the application!")
        exit(0)
