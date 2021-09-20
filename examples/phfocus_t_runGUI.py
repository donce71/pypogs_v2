"""
Example of how to set up the telescope with the CLI before starting GUI.
"""
import sys
sys.path.append('..')
import os.path
from os import path

import pypogs
from pathlib import Path

sys = pypogs.System()
try:

    # LOAD
    sys.add_fine_camera(model='phfocus', identity='autoIP')

    # FINE
    sys.fine_camera.exposure_time = 100 # 10FPS interval is 100ms
    sys.fine_camera.gain = 1
    sys.fine_camera.frame_rate = 3
    sys.fine_camera.plate_scale = .69
    sys.fine_camera.flip_x = False          #X false, Y True  - with these settings fine cam connector is on the close side to the telescope
    sys.fine_camera.flip_y = True
    sys.fine_track_thread.spot_tracker.max_search_radius = 100
    sys.fine_track_thread.spot_tracker.min_search_radius = 10
    sys.fine_track_thread.spot_tracker.crop = (640, 512)
    sys.fine_track_thread.spot_tracker.spot_min_sum = 500
    sys.fine_track_thread.spot_tracker.image_th = 50
    sys.fine_track_thread.spot_tracker.bg_subtract_mode = 'global_median'
    sys.fine_track_thread.spot_tracker.fails_to_drop = 20
    sys.fine_track_thread.spot_tracker.smoothing_parameter = 20  #SD calculation window size (smaller -> faster SD will change)
    sys.fine_track_thread.spot_tracker.rmse_smoothing_parameter = 20
    sys.fine_track_thread.spot_tracker.spot_max_axis_ratio = None
    sys.fine_track_thread.feedforward_threshold = 5
    sys.fine_track_thread.img_save_frequency = 0.1
    sys.fine_track_thread.image_folder = Path(r'C:\Users\Donatas Miklusis\Documents\Observations_pic\fine')

    pypogs.GUI(sys, 500)


except Exception:
    raise
finally:
    gc_loop_stop = True
    sys.deinitialize()

