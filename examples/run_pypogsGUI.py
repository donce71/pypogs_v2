# -*- coding: utf-8 -*-
"""
Run the pypogs GUI
==================

Run this script (i.e. type python run_pypogsGUI.py in a termnial window) to start the pypogs Graphical User Interface.
"""
import sys
import IPython
sys.path.append('..')

import pypogs

sys = pypogs.System()


try:
    # IPython.embed(colors='neutral')
    pypogs.GUI(sys, 500)

except Exception:
    raise
finally:
    sys.deinitialize()

