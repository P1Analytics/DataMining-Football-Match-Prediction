import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import src.gui.MainGui as MainGui
import src.util.util as util


if __name__ == "__main__":
    util.init_logger()
    MainGui.run()

