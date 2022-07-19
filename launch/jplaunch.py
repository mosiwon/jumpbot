import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from scripts import GazeboRosPaths
import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import ThisLaunchFileDir,LaunchConfiguration
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    model_path = GazeboRosPaths.get_paths()

    pkg_dir = ('/home/mosiwon/ros2/ws_jbbot/jumpbot')
    env = {
        "GAZEBO_MODEL_PATH": model_path,
    }

    sdf_prefix = ('/home/mosiwon/ros2/ws_jbbot/jumpbot')
    sdf_file = os.path.join(sdf_prefix, "urdf", "jumpbot.sdf")

    world_prefix = ('/home/mosiwon/ros2/ws_jbbot/jumpbot')
    world_file = os.path.join(world_prefix, "gazebo_world", "seho.world")


    return LaunchDescription(
        [
            ExecuteProcess(
                cmd=[
                    "gazebo",
                    "-s",
                    "libgazebo_ros_init.so",
                    "-s",
                    "libgazebo_ros_factory.so",
                     world_file,
                ],
                output="screen",
                additional_env=env,
            ),
            Node(
                package="gazebo_ros",
                node_executable="spawn_entity.py",
                arguments=[
                    "-entity",
                    "jumpbot",
                    "-x",
                    "-1",
                    "-y",
                    "0",
                    "-z",
                    ".41",
                    "-b",
                    "-file",
                    sdf_file,
                ],
            ),
            Node(
                package="robot_state_publisher",
                node_executable="robot_state_publisher",
                output="screen",
                arguments=[sdf_file],
            ),
          
        ]
    )
