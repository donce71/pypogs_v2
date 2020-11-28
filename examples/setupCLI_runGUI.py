"""
Example of how to set up the telescope with the CLI before starting GUI.
"""
import sys
sys.path.append('..')

import pypogs
from pathlib import Path

sys = pypogs.System()
try:

    # LOAD
    sys.add_coarse_camera(model='ptgrey', identity='18285284')
    sys.add_star_camera_from_coarse()
    sys.add_fine_camera(model='ptgrey', identity='18285254')
    sys.add_mount(model='Celestron', identity='COM7')
    sys.alignment.set_location_lat_lon(lat=52.1253, lon=4.4956, height=44) #Zouterwoede
    # sys.alignment.set_location_lat_lon(lat=52.2155, lon=4.4194, height=45) #ESTEC football field (0m MSL)
    sys.target.set_target_from_ra_dec(40.4125, 89.26417) #Polaris

    #Load alignment from previous session observation
    csv_file = r'C:\ESA Telescope\pypogs-master\pypogs\data\2020-11-24T172921_System_star_align.csv'
    alignment_list = sys.get_alignment_list_from_csv(csv_file)
    sys.alignment.set_alignment_from_observations(alignment_list)

	# sys.target.set_target_from_ra_dec(40.4125, 89.26417) #Polaris
    # sys.target.set_target_from_ra_dec(37.6792, 14.3467) # Uranas
    # sys.target.set_target_from_ra_dec(288.6667, -22.7550) # Jupiter
    # sys.target.set_target_from_ra_dec(297.1458, -21.4019) # Saturn
	
    # COARSE/STAR
	#sys.coarse_camera.exposure_time_auto = False
    #sys.coarse_track_thread.spot_tracker.image_th = 10000
    sys.coarse_camera.exposure_time = 450 #450
    sys.coarse_camera.gain = 0
    sys.coarse_camera.frame_rate = 2
    sys.coarse_camera.binning = 2
    sys.coarse_camera.plate_scale = 20.3
    sys.coarse_track_thread.goal_x_y = [0, 0]
    sys.coarse_track_thread.spot_tracker.max_search_radius = 500
    sys.coarse_track_thread.spot_tracker.min_search_radius = 200
    sys.coarse_track_thread.spot_tracker.crop = None #(256,256)         #Pakeisti i None
    sys.coarse_track_thread.spot_tracker.spot_min_sum = 500
    sys.coarse_track_thread.spot_tracker.bg_subtract_mode = 'local_median'
    sys.coarse_track_thread.spot_tracker.sigma_mode = 'local_median_abs'
    sys.coarse_track_thread.spot_tracker.fails_to_drop = 10
    sys.coarse_track_thread.spot_tracker.smoothing_parameter = 8 #SD calculation window size (smaller -> faster SD will change)
    sys.coarse_track_thread.spot_tracker.rmse_smoothing_parameter = 8
    sys.coarse_track_thread.feedforward_threshold = 10
    sys.coarse_track_thread.img_save_frequency = 3
    sys.coarse_track_thread.image_folder = Path(r'C:\Users\Donatas Miklusis\Documents\Observations_pic')

    # FINE
    sys.fine_camera.exposure_time = 60
    sys.fine_camera.gain = 0
    sys.fine_camera.frame_rate = 10
    sys.fine_camera.binning = 2
    sys.fine_camera.plate_scale = .30
    sys.fine_camera.flip_x = True
    sys.fine_track_thread.spot_tracker.max_search_radius = 100
    sys.fine_track_thread.spot_tracker.min_search_radius = 10
    sys.fine_track_thread.spot_tracker.crop = (256, 256)
    sys.fine_track_thread.spot_tracker.spot_min_sum = 500
    sys.fine_track_thread.spot_tracker.image_th = 50
    sys.fine_track_thread.spot_tracker.bg_subtract_mode = 'global_median'
    sys.fine_track_thread.spot_tracker.fails_to_drop = 20
    sys.fine_track_thread.spot_tracker.smoothing_parameter = 20  #SD calculation window size (smaller -> faster SD will change)
    sys.fine_track_thread.spot_tracker.rmse_smoothing_parameter = 20
    sys.fine_track_thread.spot_tracker.spot_max_axis_ratio = None
    sys.fine_track_thread.feedforward_threshold = 5
    sys.fine_track_thread.img_save_frequency = 3
    sys.fine_track_thread.image_folder = Path(r'C:\Users\Donatas Miklusis\Documents\Observations_pic')

    # FEEDBACK
    sys.control_loop_thread.integral_max_add = 30
    sys.control_loop_thread.integral_max_subtract = 30
    sys.control_loop_thread.integral_min_rate = 5
    sys.control_loop_thread.OL_P = 1
    sys.control_loop_thread.OL_I = 10
    sys.control_loop_thread.OL_speed_limit = 4*3600
    sys.control_loop_thread.CCL_P = 1
    sys.control_loop_thread.CCL_I = 10
    sys.control_loop_thread.CCL_speed_limit = 360
    sys.control_loop_thread.CCL_transition_th = 100
    sys.control_loop_thread.FCL_P = 2
    sys.control_loop_thread.FCL_I = 10
    sys.control_loop_thread.FCL_speed_limit = 180
    sys.control_loop_thread.FCL_transition_th = 50
    sys.control_loop_thread.CTFSP_spacing = 100
    sys.control_loop_thread.CTFSP_speed = 50
    sys.control_loop_thread.CTFSP_max_radius = 500
    sys.control_loop_thread.CTFSP_transition_th = 20
    sys.control_loop_thread.CTFSP_auto_update_CCL_goal = True
    sys.control_loop_thread.CTFSP_auto_update_CCL_goal_th = 10
    sys.control_loop_thread.CTFSP_disable_after_goal_update = True

    pypogs.GUI(sys, 500)
except Exception:
    raise
finally:
    gc_loop_stop = True
    sys.deinitialize()
