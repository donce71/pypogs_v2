import pypogs
import time
import matplotlib.pyplot as plt

# Create instance and set parameters (will auto initialise)
try:
    cam = pypogs.Camera(model='phfocus', identity='AutoIP', name='CoarseCam')
    time.sleep(1)
    cam.frame_rate = 2
    print('frame rate:', cam.frame_rate)  # hz
    # # Start acquisition
    notemap = cam._phfocus_ia.remote_device.node_map
    print(notemap.ExposureTime.value)

    cam.start()
    time.sleep(3)

    print('Height before',notemap.Height.value)

    cam.size_readout = (544, 500)
    print('Height after', notemap.Height.value)
    cam.start()
    time.sleep(3)

    # time.sleep(3)
    # cam.start()
    # cam.frame_rate = 10
    # print('frame rate:', cam.frame_rate)  # hz
    #
    # try:
    #     while True:
    #         time.sleep(1.0)
    # except KeyboardInterrupt:
    #     pass

    # data = cam._phfocus_grab()
    # plt.imshow(data)
    # plt.show()

    cam.deinitialize()
    print('Exit program')

except Exception as exc:
    cam.deinitialize()
    print('Error runtime')
