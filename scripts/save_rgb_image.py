# Subscribe to the ROS 2 RGB topic 
# and save an image to your computer for later processing.


# tasks this script performs:
# 1. Subscribe to the RealSense D435 RGB stream.
# 2. Save the first image immediately after receiving it.
# 3. Wait 2 seconds, then save the second image.
# 4. Wait another 2 seconds, then save the third image.
# 5. Automatically stop after saving exactly 3 images.

import time
from datetime import datetime
from pathlib import Path

import cv2
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image


class RGBImageSaver(Node):
    def __init__(self):
        super().__init__("rgb_image_saver")

        self.bridge = CvBridge()
        self.interval = 2.0
        self.max_images = 3
        self.saved_count = 0
        self.last_saved = None

        self.output_dir = Path("/workspace/captures")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.subscription = self.create_subscription(
            Image,
            "/camera/camera/color/image_raw",
            self.image_callback,
            qos_profile_sensor_data,
        )

        self.get_logger().info("Waiting for RGB images...")

    def image_callback(self, msg):
        if self.saved_count >= self.max_images:
            return

        now = time.monotonic()

        if (
            self.last_saved is not None
            and now - self.last_saved < self.interval
        ):
            return

        frame = self.bridge.imgmsg_to_cv2(
            msg, desired_encoding="bgr8"
        )

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = self.output_dir / f"rgb_{timestamp}.png"

        if cv2.imwrite(str(filename), frame):
            self.saved_count += 1
            self.last_saved = now
            self.get_logger().info(
                f"Saved image {self.saved_count}/{self.max_images}: {filename}"
            )
        else:
            self.get_logger().error(f"Failed to save: {filename}")


def main():
    rclpy.init()
    node = RGBImageSaver()

    try:
        while rclpy.ok() and node.saved_count < node.max_images:
            rclpy.spin_once(node, timeout_sec=0.1)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
