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
    sys.add_coarse_camera(model='phfocus', identity='autoIP')
    sys.add_star_camera_from_coarse()

    # COARSE/STARV
	#sys.coarse_camera.exposure_time_auto = False
    #sys.coarse_track_thread.spot_tracker.image_th = 10000
    sys.coarse_camera.exposure_time = 45 #450
    sys.coarse_camera.gain = 1
    sys.coarse_camera.frame_rate = 2
    # sys.coarse_camera.binning = 2
    sys.coarse_camera.plate_scale = 20.3
    sys.coarse_track_thread.goal_x_y = [0, 0]
    sys.coarse_track_thread.spot_tracker.max_search_radius = 500
    sys.coarse_track_thread.spot_tracker.min_search_radius = 200
    sys.coarse_track_thread.spot_tracker.crop = (512, 512) #None #None  #(256,256)         #Pakeisti i None
    sys.coarse_track_thread.spot_tracker.spot_min_sum = 500
    sys.coarse_track_thread.spot_tracker.bg_subtract_mode = 'local_median'
    sys.coarse_track_thread.spot_tracker.sigma_mode = 'local_median_abs'
    sys.coarse_track_thread.spot_tracker.fails_to_drop = 10
    sys.coarse_track_thread.spot_tracker.smoothing_parameter = 4 #SD calculation window size (smaller -> faster SD will change)
    sys.coarse_track_thread.spot_tracker.rmse_smoothing_parameter = 8
    sys.coarse_track_thread.feedforward_threshold = 10
    sys.coarse_track_thread.img_save_frequency = 0.1
    sys.coarse_track_thread.image_folder = Path(r'C:\Users\Donatas Miklusis\Documents\Observations_pic\coarse')

    pypogs.GUI(sys, 500)


except Exception:
    raise
finally:
    gc_loop_stop = True
    sys.deinitialize()

