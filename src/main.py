import sys
import os
import argparse

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import src.gui.MainGui as MainGui
import src.util.util as util
import src.util.SQLLite as SQLLite
import src.application.Crawl.Crawl as Crawl
import src.application.MachineLearning.prediction_accuracy.Predictor as Predictor

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Score Prediction Application')
    # --no-crawl
    parser.add_argument('--no-crawl', dest='do_crawl', action='store_false',
                        help='do not crawl on the start up of the application')
    parser.set_defaults(do_crawl=True)

    # --no-index
    parser.add_argument('--no-index', dest='do_index', action='store_false',
                        help='do not index on the start up of the application')
    parser.set_defaults(do_index=True)

    # -d
    parser.add_argument('-v', dest='debug', action='store_true',
                        help='turn debug on')
    parser.set_defaults(debug=False)
    args = parser.parse_args()

    if not SQLLite.init_database():
        print("IMPORT DATABASE!!!")
        exit(-1)

    Predictor.init_predictor()

    if args.debug:
        util.init_logger(10)
    else:
        util.init_logger(20)

    if args.do_index:
        util.indexing()

    if args.do_crawl:
        Crawl.run_init_crawl()
    try:
        MainGui.run()
    except KeyboardInterrupt:
        print("\nClosing the application!")
        exit(0)
