import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
import numpy as np
from ultralytics import YOLO

class YoloDetectorNode(Node):
    def __init__(self):
        super().__init__('yolo_detector_node')
        
        self.get_logger().info('Loading YOLOv8 model...')
        self.model = YOLO('yolov8n.pt')

        # Subscribe to Gazebo camera topic
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        # Publisher for annotated camera stream
        self.publisher_ = self.create_publisher(Image, '/yolo/annotated_image', 10)
        self.get_logger().info('YOLOv8 Detector Node operational!')

    def image_callback(self, msg):
        try:
            # 1. Direct raw byte extraction without cv_bridge
            height = msg.height
            width = msg.width
            
            # Calculate bytes per pixel dynamically
            total_bytes = len(msg.data)
            bytes_per_pixel = total_bytes // (height * width) if (height * width) > 0 else 3

            raw_data = np.frombuffer(msg.data, dtype=np.uint8)

            if bytes_per_pixel == 4:
                frame = raw_data.reshape((height, width, 4))
                cv_image = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
            elif bytes_per_pixel == 3:
                frame = raw_data.reshape((height, width, 3))
                cv_image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            else:
                self.get_logger().error(f'Unexpected image channels: {bytes_per_pixel}')
                return

            # 2. Run YOLO inference
            results = self.model(cv_image, verbose=False)

            # 3. Get annotated frame (BGR NumPy array)
            annotated_frame = results[0].plot()

            # 4. Construct outgoing ROS Image message manually (No cv_bridge!)
            out_msg = Image()
            out_msg.header = msg.header
            out_msg.height = annotated_frame.shape[0]
            out_msg.width = annotated_frame.shape[1]
            out_msg.encoding = 'bgr8'
            out_msg.is_bigendian = 0
            out_msg.step = annotated_frame.shape[1] * 3
            out_msg.data = annotated_frame.tobytes()

            self.publisher_.publish(out_msg)

        except Exception as e:
            # Full exception trace to pin down the exact line if it fails
            import traceback
            self.get_logger().error(f'Error details:\n{traceback.format_exc()}')

def main(args=None):
    rclpy.init(args=args)
    node = YoloDetectorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()