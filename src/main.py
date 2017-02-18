import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import src.gui.MainGui as MainGui
import src.util.util as util
import src.util.SQLLite as SQLLite


if __name__ == "__main__":
    util.init_logger()
    SQLLite.init_database()
    try:
        MainGui.run()
    except KeyboardInterrupt:
        print("\nClosing the applicarion!")
        exit(0)

