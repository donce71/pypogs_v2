import pypogs
import time

# Create instance and set parameters (will auto initialise)
cam = pypogs.Camera(model='ptgrey', identity='18285254', name='CoarseCam')
cam.gain = 0  # decibel
cam.exposure_time = 100  # milliseconds
cam.frame_rate_auto = True
# Start acquisition
cam.start()
# Wait for a while
time.sleep(2)
# Read the latest image
img = cam.get_latest_image()
# Stop the acquisition
cam.stop()
# Release the hardware
cam.deinitialize()