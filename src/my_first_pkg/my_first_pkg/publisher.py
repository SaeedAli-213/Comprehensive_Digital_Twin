import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

import carla
import numpy as np

def spawn_vehicle(world):
    blueprint = world.get_blueprint_library().filter('model3')[0]
    spawn_point = world.get_map().get_spawn_points()[0]
    vehicle = world.spawn_actor(blueprint, spawn_point)
    vehicle.set_autopilot(True)
    return vehicle

class CarlaPublisherNode(Node):
    def __init__(self):
        super().__init__('carla_publisher')
        self.client = carla.Client("localhost", 2000)
        self.client.set_timeout(10.0)
        self.world = self.client.get_world()
        self.vehicle = spawn_vehicle(self.world)

        # ROS publishers
        self.speed_pub = self.create_publisher(Float64, '/carla/vehicle/speed', 10)
        self.soc_pub   = self.create_publisher(Float64, '/carla/soc', 10)
        self.posx_pub  = self.create_publisher(Float64, '/carla/posx', 10)
        self.posy_pub  = self.create_publisher(Float64, '/carla/posy', 10)
        self.front_pub = self.create_publisher(Image,   '/carla/camera/front/image_raw', 10)
        self.back_pub  = self.create_publisher(Image,   '/carla/camera/back/image_raw',  10)

        # Bridge for converting OpenCV images to ROS
        self.br = CvBridge()

        # Latest images
        self.latest_front = None
        self.latest_back  = None

        # Setup cameras
        self._setup_cameras()

        # Timer: publish telemetry + images every 0.1 s
        self.create_timer(0.1, self._publish_data)

    def _setup_cameras(self):
        bp_lib = self.world.get_blueprint_library()
        cam_bp = bp_lib.find("sensor.camera.rgb")
        cam_bp.set_attribute("image_size_x", "320")
        cam_bp.set_attribute("image_size_y", "180")
        cam_bp.set_attribute("fov", "90")

        # Front camera
        front_tf = carla.Transform(carla.Location(x=4, z=1.6))
        self.front_sensor = self.world.spawn_actor(cam_bp, front_tf, attach_to=self.vehicle)
        self.front_sensor.listen(self._on_front_image)

        # Back camera
        back_tf = carla.Transform(
            carla.Location(x=-4, z=1.6),
            carla.Rotation(yaw=180)
        )
        self.back_sensor = self.world.spawn_actor(cam_bp, back_tf, attach_to=self.vehicle)
        self.back_sensor.listen(self._on_back_image)

    def _on_front_image(self, image):
        # CARLA gives BGRA in raw_data; convert to RGB numpy array
        arr = np.frombuffer(image.raw_data, dtype=np.uint8)
        arr = arr.reshape((image.height, image.width, 4))
        self.latest_front = arr[:, :, :3]  # drop alpha

    def _on_back_image(self, image):
        arr = np.frombuffer(image.raw_data, dtype=np.uint8)
        arr = arr.reshape((image.height, image.width, 4))
        self.latest_back = arr[:, :, :3]

    def _publish_data(self):
        # --- telemetry ---
        tr = self.vehicle.get_transform()
        vel = self.vehicle.get_velocity()
        speed_mps = (vel.x**2 + vel.y**2 + vel.z**2) ** 0.5
        speed_kph = speed_mps * 3.6

        self.speed_pub.publish(Float64(data=speed_kph))
        self.soc_pub.publish(Float64(data=80.0))          # dummy SOC
        self.posx_pub.publish(Float64(data=tr.location.x))
        self.posy_pub.publish(Float64(data=tr.location.y))

        # --- front image ---
        if self.latest_front is not None:
            try:
                img_msg = self.br.cv2_to_imgmsg(self.latest_front, "rgb8")
                img_msg.header.stamp = self.get_clock().now().to_msg()
                self.front_pub.publish(img_msg)
            except Exception as e:
                self.get_logger().error(f"Front publish error: {e}")

        # --- back image ---
        if self.latest_back is not None:
            try:
                img_msg = self.br.cv2_to_imgmsg(self.latest_back, "rgb8")
                img_msg.header.stamp = self.get_clock().now().to_msg()
                self.back_pub.publish(img_msg)
            except Exception as e:
                self.get_logger().error(f"Back publish error: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = CarlaPublisherNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()