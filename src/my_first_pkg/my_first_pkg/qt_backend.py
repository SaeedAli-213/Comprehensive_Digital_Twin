
# qt_backend.py
import struct
import numpy as np
import time
import cv2
from collections import deque
from PySide6.QtGui import QImage
from PySide6.QtCore import QObject, Signal, Slot, QBuffer, QByteArray, QTimer
from multiprocessing import shared_memory

def carla_to_map_coords(carla_x, carla_y, map_width, map_height, carla_bounds):
    carla_min_x, carla_max_x, carla_min_y, carla_max_y = carla_bounds
    scale_x = map_width / (carla_max_x - carla_min_x)
    scale_y = map_height / (carla_max_y - carla_min_y)
    map_x = (carla_x - carla_min_x) * scale_x
    map_y = map_height - (carla_y - carla_min_y) * scale_y
    return map_x, map_y

class BackendAPI(QObject):
    front_camera_frame_ready = Signal(str)
    back_camera_frame_ready = Signal(str)
    vehicle_speed_updated = Signal(float)
    soc_signal = Signal(float)
    positionChanged = Signal(float, float)
    map_image_ready = Signal(str)
    collision_warning_signal = Signal(str)
    critical_distance_warning_signal = Signal(str)

    CRITICAL_DISTANCE_THRESHOLD = 3.0

    def __init__(self):
        super().__init__()
        # Open shared memory blocks
        self.vehicle_shm = shared_memory.SharedMemory(name='vehicle_data')
        self.front_cam_shm = shared_memory.SharedMemory(name='front_camera')
        self.back_cam_shm = shared_memory.SharedMemory(name='back_camera')

        self.map_width = 1024
        self.map_height = 1024
        self.carla_bounds = (-200, 200, -200, 200)

        self.front_camera_queue = deque(maxlen=10)
        self.back_camera_queue = deque(maxlen=10)

        self.is_running_front = False
        self.is_running_back = False
        self.last_frame_time = time.time()


        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.poll_globals)
        self.update_timer.timeout.connect(self.start_front_camera)

        self.update_timer.start(100)


    @Slot()
    def poll_globals(self):
        # Telemetry
        self.fetch_vehicle_speed()
        self.get_soc()
        self.update_position()



    @Slot()
    def fetch_vehicle_speed(self):
        data = self.vehicle_shm.buf[0:8]
        speed = struct.unpack('d', data)[0]
        self.vehicle_speed_updated.emit(speed)

    @Slot()
    def get_soc(self):
        data = self.vehicle_shm.buf[8:16]
        soc = struct.unpack('d', data)[0]
        self.soc_signal.emit(soc)

    @Slot()
    def update_position(self):
        x_bytes = self.vehicle_shm.buf[16:24]
        y_bytes = self.vehicle_shm.buf[24:32]
        x = struct.unpack('d', x_bytes)[0]
        y = struct.unpack('d', y_bytes)[0]
        map_x, map_y = carla_to_map_coords(x, y, self.map_width, self.map_height, self.carla_bounds)
        self.positionChanged.emit(map_x, map_y)

    @Slot()
    def start_front_camera(self):
        self.is_running_front = True
        raw = self.front_cam_shm.buf[:320*180*4]
        self.process_camera_frame(raw, 'front')


    @Slot()
    def start_back_camera(self):
        self.is_running_back = True

    @Slot()
    def stop_front_camera(self):
        self.is_running_front = False

    @Slot()
    def stop_back_camera(self):
        self.is_running_back = False

    def process_camera_frame(self, raw_data: memoryview, camera_type: str):
        """
        raw_data: memoryview or bytes of length 320*180*4 (RGBA)
        camera_type: 'front' or 'back'
        """
        current_time = time.time()
        if current_time - self.last_frame_time < 0.2:
            return
        self.last_frame_time = current_time

        try:
            # Convert raw_data to numpy RGBA image


            # Create QImage for QML
            width, height = 320, 180
            bytes_per_line = width * 4
            img = QImage(raw_data, width, height, bytes_per_line, QImage.Format_RGBA8888)
            if img.isNull():
                raise ValueError('Invalid QImage')

            # Convert to PNG and base64
            buffer = QBuffer()
            buffer.open(QBuffer.ReadWrite)
            img.save(buffer, 'PNG')
            buffer.close()

            b64 = QByteArray(buffer.data()).toBase64().data().decode('utf-8')
            data_url = f'data:image/png;base64,{b64}'

            if camera_type == 'front':
                self.front_camera_frame_ready.emit(data_url)
            else:
                self.back_camera_frame_ready.emit(data_url)

        except Exception as e:
            print(f'Camera frame error: {e}')