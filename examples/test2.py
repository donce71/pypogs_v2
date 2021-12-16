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



from harvesters.core import Callback

class CameraBase:
    """TBW."""

    @abc.abstractmethod
    def is_simulating(self) -> bool:
        """TBW."""
        ...

    @abc.abstractmethod
    def is_open(self) -> bool:
        """TBW."""
        ...

    @abc.abstractmethod
    def is_acquiring(self) -> bool:
        """TBW."""
        ...

    @abc.abstractmethod
    def open(self) -> None:
        """TBW."""
        ...

    @abc.abstractmethod
    def close(self) -> None:
        """TBW."""
        ...

    @abc.abstractmethod
    def get_bits(self) -> int:
        """TBW."""
        ...

    @abc.abstractmethod
    def set_on_frame_ready(self, on_frame_ready: t.Optional[t.Callable]) -> None:
        """TBW."""
        ...

    @abc.abstractmethod
    def set_capture_state(self, new_state: t.Optional[bool] = None) -> None:
        """TBW."""
        ...

    @abc.abstractmethod
    def set_exposure_time(self, exp_in_sec: float) -> None:
        """TBW."""
        ...

    @abc.abstractmethod
    def get_exposure_time(self) -> float:
        """TBW."""
        ...

    def apply_calibration(self, data: t.Any) -> None:
        """TBW."""
        ...

    @abc.abstractmethod
    def grab_continuous(self, separate_thread: bool = False) -> None:
        """TBW."""
        ...

    @abc.abstractmethod
    def stop(self) -> None:
        """TBW."""
        ...



class Driver(CameraBase):
    """TBW."""

    def __init__(self, simulate: bool = False):
        """TBW."""
        super().__init__()
        self._log = logging.getLogger(__name__)
        self._dev = None  # type: t.Optional[t.Any]
        self._ia = None  # type: t.Optional[t.Any]
        self._on_frame_ready = None  # type: t.Optional[t.Callable]
        self._is_acquiring = False
        self._frame_num = 0
        self._th = None  # type: t.Optional[threading.Thread]
        self._is_running = False
        self._sim_stream = None
        self._simulate = simulate

    def get_id(self) -> str:
        """TBW."""
        return "???"  # self.execute('*idn?')

    @property
    def simulate(self) -> bool:
        """TBW."""
        return self._simulate

    def is_simulating(self) -> bool:
        """TBW."""
        return self._simulate

    @property
    def has_camera_link(self) -> bool:
        """TBW."""
        return False

    def apply_calibration(self, data: t.Any) -> None:
        """TBW."""

    def get_bits(self) -> int:
        """TBW."""
        result = 16
        if self._ia:
            val = self._ia.remote_device.node_map.PixelFormat.value
            if "12" in val:
                result = 12
            elif "8" in val:
                result = 8
        return result

    def is_open(self) -> bool:
        """TBW."""
        if self._simulate:
            return True
        return self._dev is not None

    def open(self) -> None:
        """TBW."""
        if self._simulate:
            return
        h = Harvester()

        locs = [
            r"~/tools/mvImpact/lib/x86_64/mvGenTLProducer.cti",
            r"C:\Program Files\MATRIX VISION\mvIMPACT Acquire\bin\x64\mvGenTLProducer.cti"
        ]
        cti = ""
        for loc in locs:
            if Path(loc).expanduser().exists():
                cti = loc
        if not cti:
            raise FileNotFoundError("Could not locate cti file: mvGenTLProducer.cti")

        cti = str(Path(cti).expanduser())
        h.add_file(cti)
        h.update()
        len(h.device_info_list)
        h.device_info_list[0]
        print("creating ia....")
        ia = h.create_image_acquirer(0)
        print("ia created")
        # ia = h.create_image_acquirer(serial_number='050200047485')
        # ia.remote_device.node_map.Width.value = 1024  # max: 1312
        # ia.remote_device.node_map.Height.value = 1024  # max: 1082
        # ia.remote_device.node_map.PixelFormat.value = 'Mono12'



        from harvesters.core import ImageAcquirer
        print(ImageAcquirer.Events.__members__)
        from harvesters.core import Callback

        class CallbackOnNewBuffer(Callback):
            def __init__(self, ia: ImageAcquirer):
                #
                super().__init__()
                #
                self._ia = ia

            def emit(self, context):
                # # You would implement this method by yourself.
                # with _ia.fetch_buffer() as buffer:
                #     # Work with the fetched buffer.
                #     print(buffer)
                print(datetime.utcnow(), "New image")

        on_new_buffer = CallbackOnNewBuffer(self)
        ia.add_callback(
            ia.Events.NEW_BUFFER_AVAILABLE,
            on_new_buffer
        )

        ia.start_acquisition(run_in_background=True)
        self._dev = h
        self._ia = ia
        self.on_new_buffer =on_new_buffer

    def close(self) -> None:
        """TBW."""
        if self._ia:
            self._ia.stop_acquisition()
            self._ia.destroy()
            self._ia = None
        if self._dev:
            self._dev.reset()
            self._dev = None
        print("Cam closed")

    def is_acquiring(self) -> bool:
        """TBW."""
        return self._is_acquiring

    def set_on_frame_ready(self, on_frame_ready: t.Optional[t.Callable]) -> None:
        """TBW."""
        self._on_frame_ready = on_frame_ready

    def set_capture_state(self, new_state: t.Optional[bool] = None) -> None:
        """TBW."""
        if new_state is None:
            new_state = not self._is_acquiring
        self._is_acquiring = new_state

    def grab(self) -> t.Any:
        """TBW."""
        if self._simulate:
            return self._sim_stream.grab()

        if self._ia:
            try:
                with self._ia.fetch_buffer(timeout=0.1) as buffer:
                    component = buffer.payload.components[0]
                    data = component.data.reshape(component.height, component.width)
                    return np.array(data)
            except TimeoutException:
                self._log.info("log error: Timeout error.")

        return None

    def stop(self) -> None:
        """TBW."""
        self._is_running = False
        if self._th:
            self._th.join()
        self._th = None

    def grab_continuous(self, separate_thread: bool = False) -> None:
        """TBW."""
        if separate_thread:
            self._th = threading.Thread(
                target=self._grab_continuous, name="GenICamGrab"
            )
            self._th.start()
        else:
            self._grab_continuous()

    def _grab_continuous(self) -> None:
        """TBW."""
        self._log.info("Entering _grab_continuous")
        self._is_running = True
        while self._is_running:
            if not self.is_open():
                print('open is false')
                break
            if not self._is_acquiring:
                print('accuare is false')
                break

            try:
                data = self.grab()
            except Exception as exc:
                self._log.error(str(exc))
                time.sleep(2.0)
                continue

            if data is not None:
                self._frame_num += 1
                if self._on_frame_ready:
                    self._on_frame_ready(self._frame_num, data)

        self._log.info("Exiting _grab_continuous")
        print("Exiting _grab_continuous")

    def set_exposure_time(self, exp_in_sec: float) -> None:
        """TBW."""
        factor = 1
        if self._ia:
            self._ia.remote_device.node_map.ExposureTime.value = exp_in_sec * factor

    def get_exposure_time(self) -> float:
        """TBW."""
        factor = 1
        if self._ia:
            return int(self._ia.remote_device.node_map.ExposureTime.value / factor)
        return 0.0

    def set_gain(self, gain: float) -> None:
        """TBW."""
        if self._ia:
            self._ia.remote_device.node_map.Gain.value = gain

    def get_gain(self) -> float:
        """TBW."""
        if self._ia:
            return self._ia.remote_device.node_map.Gain.value
        return 0.0

    def set_pixel_format(self, pixel_format: str) -> None:
        """TBW."""
        if self._ia:
            self._ia.remote_device.node_map.PixelFormat.value = pixel_format

    def get_pixel_format(self) -> str:
        """TBW."""
        if self._ia:
            return self._ia.remote_device.node_map.PixelFormat.value
        return "Mono8"

    def set_framerate(self, framerate: float) -> None:
        """TBW."""
        if self._ia:
            self._ia.remote_device.node_map.AcquisitionFrameRate.value = framerate

    def get_framerate(self) -> float:
        """TBW."""
        print('Nodes:', dir(self._ia.remote_device.node_map))

        if self._ia:
            # print(self._ia.remote_device.node_map.AcquisitionFrameRateEnable.value)
            # self._ia.remote_device.node_map.AcquisitionFrameRateMode.value = 'True'

            return self._ia.remote_device.node_map.AcquisitionFrameRateMax.value
        return 0.0

def run_camera() -> None:
    """TBW."""
    cam = Driver()
    cam.open()
    time.sleep(1)

    ex_time = cam.get_exposure_time()
    f_rate = cam.get_framerate()
    print('ex time:', ex_time, 'framerate:', f_rate)

    # cam.set_exposure_time(1000)
    # cam.set_framerate(10)
    #
    # ex_time = cam.get_exposure_time()
    # f_rate=cam.get_framerate()
    # print('NEW: ex time:', ex_time, 'framerate:', f_rate)
    time.sleep(2)

    # data = cam.grab()
    #
    # if data is not None:
    #     plt.imshow(data)
    #     plt.show()
    #cam.close()




def frame_ready(frame_num, data):
    print(frame_num, data.shape, 'max:', np.max(data))

def main():
    cam = Driver()
    cam.open()
    time.sleep(1)

    cam.set_framerate(2)

    cam.set_capture_state(True)
    cam.set_on_frame_ready(on_frame_ready=frame_ready)
    cam.grab_continuous(separate_thread=True)

    try:
        while True:
            time.sleep(1.0)
    except KeyboardInterrupt:
        pass

    # data = cam.grab()
    #
    # plt.imshow(data)
    # plt.show()

    cam.close()



if __name__ == "__main__":
    try:
        run_camera()
    except:
        pass
        print("error")
    run_camera()

    #main()