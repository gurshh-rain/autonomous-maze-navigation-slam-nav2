import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from sensor_msgs.msg import PointCloud2
from laser_geometry import LaserProjection


class Lidar3DVisualizer(Node):
    def __init__(self):
        super().__init__('lidar_3d_visualizer')
        self.laser_projection = LaserProjection()
        self.pc2_pub = self.create_publisher(PointCloud2, '/lidar_3d_scan', 10)
        self.scan_sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )
        self.get_logger().info('3D LiDAR visualizer node started...')

    def scan_callback(self, msg):
        pc2 = self.laser_projection.projectLaser(msg)
        pc2.header = msg.header
        self.pc2_pub.publish(pc2)


def main(args=None):
    rclpy.init(args=args)
    node = Lidar3DVisualizer()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
