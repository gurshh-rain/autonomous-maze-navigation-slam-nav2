# Autonomous Maze Navigation with SLAM and Nav2

Autonomous maze navigation for a LiDAR equipped mobile robot in ROS 2. The robot uses SLAM to build a map of an unknown maze in real time and Nav2 to plan and execute paths through it, with RViz2 used for live visualization of the map, the robot's pose, and the planned routes.

## About

This project implements a full sense, map, and navigate pipeline for a differential drive robot exploring a maze it has never seen before. A 2D LiDAR scanner feeds range data into a SLAM node, which builds an occupancy grid map of the environment and localizes the robot within it. Once a usable map exists, the Nav2 stack takes over, computing collision free paths from the robot's current position to a goal pose and driving it there while continuously reacting to newly discovered obstacles. The `lidar_robot` package contains the robot description, sensor configuration, and navigation code, written in a mix of C++ and Python and structured with object oriented design so that sensing, mapping, and navigation logic stay cleanly separated.

## Features

- Real time simultaneous localization and mapping (SLAM) from 2D LiDAR data
- Autonomous path planning and execution through the Nav2 navigation stack
- Live visualization of the map, robot pose, LiDAR scans, and planned paths in RViz2
- Modular, object oriented C++ and Python nodes for sensing, mapping, and navigation
- Designed for maze style environments with narrow corridors and dead ends

## Project structure

```
.
├── lidar_robot/     # Main ROS 2 package: robot description, nodes, and config
├── build/           # Colcon build artifacts (generated, not tracked for edits)
├── install/         # Colcon install space (generated, not tracked for edits)
├── log/             # Colcon build and runtime logs (generated)
└── README.md
```

The `build`, `install`, and `log` folders are generated automatically by `colcon build` and should not be edited directly. If you are setting this up fresh, it is worth adding them to a `.gitignore` file.

## Prerequisites

- Ubuntu with a supported ROS 2 distribution installed (e.g. Humble or Jazzy)
- `colcon` build tools
- Nav2 (`navigation2` and `nav2_bringup`)
- A SLAM implementation such as `slam_toolbox`
- RViz2 for visualization
- Python 3 and a C++ compiler toolchain (for the mixed C++/Python nodes)

Install the core ROS 2 dependencies (replace `<distro>` with your ROS 2 distribution, e.g. `humble`):

```bash
sudo apt update
sudo apt install ros-<distro>-navigation2 ros-<distro>-nav2-bringup \
                  ros-<distro>-slam-toolbox ros-<distro>-rviz2
```

## Installation

1. Clone this repository into the `src` directory of a ROS 2 workspace:

   ```bash
   mkdir -p ~/ros2_ws/src
   cd ~/ros2_ws/src
   git clone https://github.com/gurshh-rain/autonomous-maze-navigation-slam-nav2.git
   ```

2. Build the workspace with `colcon`:

   ```bash
   cd ~/ros2_ws
   colcon build
   ```

3. Source the workspace:

   ```bash
   source install/setup.bash
   ```

## Usage

The typical workflow is to first build a map of the maze with SLAM, then hand off to Nav2 for autonomous navigation.

1. Launch the robot and its sensors (adjust the launch file name to match your setup):

   ```bash
   ros2 launch lidar_robot robot.launch.py
   ```

2. Launch SLAM to start building a map of the maze:

   ```bash
   ros2 launch lidar_robot slam.launch.py
   ```

3. Once a map has been built, launch Nav2 to enable autonomous navigation:

   ```bash
   ros2 launch lidar_robot navigation.launch.py
   ```

4. Open RViz2 to visualize the map, the robot, and the LiDAR scan, and use the "2D Goal Pose" tool to send the robot a navigation goal:

   ```bash
   rviz2
   ```

5. Optionally, save the completed map for future navigation runs:

   ```bash
   ros2 run nav2_map_server map_saver_cli -f ~/maze_map
   ```

Adjust the launch file names and paths above to match the ones defined inside `lidar_robot`.

## Configuration

Robot specific and navigation specific parameters (costmaps, planner and controller settings, SLAM parameters) live inside the `lidar_robot` package's config files. Tune these to match your robot's footprint, sensor placement, and the scale of your maze.

## Contributing

Issues and pull requests are welcome. If you plan a larger change, please open an issue first to discuss what you would like to do.

## License

No license has been specified yet. Add a `LICENSE` file to clarify how others may use this project.
