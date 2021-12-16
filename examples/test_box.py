"""Image acquisition library for GenICam compliant cameras & GenTL Producers."""
import abc
import logging
import threading
import time
import typing as t
from datetime import datetime
from pathlib import Path

import harvesters.core
import numpy as np
from harvesters.core import Harvester, TimeoutException  # type: ignore
import matplotlib.pyplot as plt



ra = "-030031"
dec = "-891718"
if ((ra[0:1])=="-"):
    ra = ra[1:7]
    ra = int(ra[0:2]) + int(ra[2:4]) / 60 + int(ra[4:6]) / 3600
    ra = ra * 15*(-1)
else:
    ra = int(ra[0:2]) + int(ra[2:4]) / 60 + int(ra[4:6]) / 3600
    ra = ra * 15

if ((dec[0:1])=="-"):
    dec = dec[1:7]
    dec =(-1)* (int(dec[0:2]) + int(dec[2:4]) / 60 + int(dec[4:6]) / 3600)
else:
    dec = int(dec[0:2]) + int(dec[2:4]) / 60 + int(dec[4:6]) / 3600
print(dec)