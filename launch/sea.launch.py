from launch_ros.actions import Node
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource

from ament_index_python import get_package_share_directory

def generate_launch_description():
    # include another launch file
    launch_include = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(get_package_share_directory('stonefish_ros2') + \
                                      '/launch/stonefish_simulator.launch.py'),
        launch_arguments={
            'simulation_data': get_package_share_directory('narval_stonefish')+'/data/',
            'scenario_desc': get_package_share_directory('narval_stonefish')+'/scenarios/sea.scn',
            'simulation_rate': '100.0',
            'window_res_x': '1920',
            'window_res_y': '1080',
            'rendering_quality': 'high',
        }.items()
    )

    return LaunchDescription([
        launch_include,
    ])