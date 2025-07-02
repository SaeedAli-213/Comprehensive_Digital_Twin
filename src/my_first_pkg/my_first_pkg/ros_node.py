# ros_node.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from multiprocessing import shared_memory
import struct
import cv2  # OpenCV for display

class ROSDataSubscriber(Node):
    def __init__(self):
        super().__init__('ros_backend_node')
        self.bridge = CvBridge()

        # Shared memory for telemetry (4 Float64 values = 32 bytes)
        self.main_shm = shared_memory.SharedMemory(name='vehicle_data', create=True, size=32)
        # Shared memory for camera frames: RGBA 320x180 = 320*180*4 = 230400 bytes
        self.front_cam_shm = shared_memory.SharedMemory(name='front_camera', create=True, size=320*180*4)
        self.back_cam_shm  = shared_memory.SharedMemory(name='back_camera',  create=True, size=320*180*4)

        # Subscriptions
        self.create_subscription(Float64, '/carla/vehicle/speed', self.speed_callback,        10)
        self.create_subscription(Float64, '/carla/soc',           self.soc_callback,          10)
        self.create_subscription(Float64, '/carla/posx',         self.posx_callback,        10)
        self.create_subscription(Float64, '/carla/posy',         self.posy_callback,        10)
        self.create_subscription(Image,    '/carla/camera/front/image_raw', self.front_camera_callback, 10)
        self.create_subscription(Image,    '/carla/camera/back/image_raw',  self.back_camera_callback,  10)

    def write_float(self, offset, value):
        self.main_shm.buf[offset:offset+8] = struct.pack('d', value)

    def speed_callback(self, msg):
        self.write_float(0, msg.data)
        self.get_logger().info(f"Speed: {msg.data}")

    def soc_callback(self, msg):
        self.write_float(8, msg.data)
        self.get_logger().info(f"SOC: {msg.data}")

    def posx_callback(self, msg):
        self.write_float(16, msg.data)
        self.get_logger().info(f"PosX: {msg.data}")

    def posy_callback(self, msg):
        self.write_float(24, msg.data)
        self.get_logger().info(f"PosY: {msg.data}")

    def front_camera_callback(self, msg):
        try:
            # Convert ROS Image to BGR for OpenCV
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            # Display image

            # Also write RGBA bytes to shared memory if needed
            rgba = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGBA)
            self.front_cam_shm.buf[:rgba.nbytes] = rgba.tobytes()
        except Exception as e:
            self.get_logger().error(f"Front camera error: {e}")

    def back_camera_callback(self, msg):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

            rgba = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGBA)
            self.back_cam_shm.buf[:rgba.nbytes] = rgba.tobytes()
        except Exception as e:
            self.get_logger().error(f"Back camera error: {e}")

    def destroy_all(self):
        # Clean up shared memory on shutdown
        self.main_shm.close()
        self.main_shm.unlink()
        self.front_cam_shm.close()
        self.front_cam_shm.unlink()
        self.back_cam_shm.close()
        self.back_cam_shm.unlink()


def run_ros_node():
    rclpy.init()
    node = ROSDataSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_all()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    run_ros_node()