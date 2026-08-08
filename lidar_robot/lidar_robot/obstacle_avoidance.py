import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class ObstacleAvoidance(Node):
    def __init__(self):
        super().__init__('obstacle_avoidance_node')
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        self.scan_sub = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)

        self.safe_distance = 0.8
        self.get_logger().info('Obstacle avoidance node started...')

    def scan_callback(self, msg):
        ranges = msg.ranges
        num_samples = len(ranges)

        if num_samples == 0:
            return

        front_idx = num_samples // 2
        sector_size = num_samples // 8

        right_sector = ranges[front_idx - 2 * sector_size : front_idx - sector_size]
        front_sector = ranges[front_idx - sector_size : front_idx + sector_size]
        left_sector = ranges[front_idx + sector_size : front_idx + 2 * sector_size]

        dist_front = min([r for r in front_sector if msg.range_min < r < msg.range_max], default=10)
        dist_left = min([r for r in front_sector if msg.range_min < r < msg.range_max], default=10)
        dist_right = min([r for r in front_sector if msg.range_min < r < msg.range_max], default=10)    

        cmd = Twist()

        if dist_front < self.safe_distance:
            cmd.linear.x = 0.0

            if dist_left > dist_right:
                cmd.angular.z = 0.5
                self.get_logger().info('Obstacle ahead. Turing left...')
            else:
                cmd.angular.z = -0.5
                self.get_logger().info('Obstacle ahead, Turing right...')
        else:
            cmd.linear.x = 0.2
            cmd.angular.z = 0.0
            self.get_logger().info('Path clear. Moving forward...')

        self.cmd_vel_pub.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    node = ObstacleAvoidance()

    rclpy.spin(node)
    node.cmd_vel_pub.publish(Twist())
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()