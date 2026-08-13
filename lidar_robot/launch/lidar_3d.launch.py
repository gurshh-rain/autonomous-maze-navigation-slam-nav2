import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    pkg_name = 'lidar_robot'
    pkg_share = get_package_share_directory(pkg_name)

    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_share, 'launch', 'gazebo.launch.py')
        )
    )

    lidar_3d_visualizer = Node(
        package=pkg_name,
        executable='lidar_3d_visualizer',
        name='lidar_3d_visualizer',
        output='screen',
        parameters=[{'use_sim_time': True}]
    )

    rviz_config = os.path.join(pkg_share, 'rviz', 'lidar_3d.rviz')
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config],
        output='screen',
        parameters=[{'use_sim_time': True}]
    )

    return LaunchDescription([
        gazebo_launch,
        lidar_3d_visualizer,
        rviz_node
    ])
