import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import src.gui.MainGui as MainGui


if __name__ == "__main__":
    MainGui.run()

