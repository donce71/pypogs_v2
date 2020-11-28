# -*- coding: utf-8 -*-
"""
Run the pypogs GUI
==================

Run this script (i.e. type python run_pypogsGUI.py in a termnial window) to start the pypogs Graphical User Interface.
"""
import sys
sys.path.append('..')

import pypogs

sys = pypogs.System()
sys.add_coarse_camera(model='ptgrey', identity='18285284')

try:
    pypogs.GUI(sys, 500)
except Exception:
    raise
finally:
    sys.deinitialize()

