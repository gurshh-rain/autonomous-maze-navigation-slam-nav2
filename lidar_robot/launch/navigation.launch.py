import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_name = 'lidar_robot'
    pkg_share = get_package_share_directory(pkg_name)
    nav2_share = get_package_share_directory('nav2_bringup')

    map_file = os.path.join(pkg_share, 'maps', 'maze_map.yaml')
    params_file = os.path.join(pkg_share, 'config', 'nav2_params.yaml')

    # 1. Gazebo Launch
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_share, 'launch', 'gazebo.launch.py')
        )
    )

    # 2. Nav2 Bringup Launch
    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_share, 'launch', 'bringup_launch.py')
        ),
        launch_arguments={
            'map': map_file,
            'params_file': params_file,
            'use_sim_time': 'true'
        }.items()
    )

    # 3. RViz2 Node
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        parameters=[{'use_sim_time': True}]
    )

    return LaunchDescription([
        gazebo_launch,
        nav2_launch,
        rviz_node
    ])