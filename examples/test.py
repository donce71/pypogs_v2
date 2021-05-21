# Standard imports:
from pathlib import Path
import logging
import sys
from threading import Thread, Event
from time import sleep, perf_counter as precision_timestamp
from datetime import datetime
from csv import writer as csv_write

# External imports:
from astropy.time import Time as apy_time
from astropy import units as apy_unit
import numpy as np
from tifffile import imwrite as tiff_write
from tifffile import imread

# Internal imports:
sys.path.append('..')  # Add one directory up to path
from tetra3 import get_centroids_from_image
# from .hardware import Camera

EPS = 10**-6  # Epsilon for use in non-zero check
DEG = chr(176)  # Degree (unicode) character

path = r'C:\Users\Donatas Miklusis\Documents\Observations_pic\coarse\2021-04-01T214134_CoarseTracker_img_61.tiff'
img = imread(path)


ret = get_centroids_from_image(img, image_th=None,
                               binary_open=True, filtsize=7,
                               crop=None, downsample=None, min_area=10,
                               max_area=None, min_sum=3000, max_sum=None,
                               max_axis_ratio=5,
                               sigma_mode='local_median_abs',
                               bg_sub_mode='local_median',
                               return_moments=False, sigma=1.5,
                               centroid_window=None)
nret = np.zeros([200,2])
i=0
for cen in ret:
    if cen[0]>300 and cen[0]<420:
        i=i+1
        nret[i]=cen