from launch_ros.actions import Node
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare

from ament_index_python import get_package_share_directory

def generate_launch_description():

    stonefish_share = FindPackageShare('narval_stonefish')
    thruster_manager_share = FindPackageShare('narval_thruster_manager')
    description_share = FindPackageShare('narval_description')
    wrench_system_share = FindPackageShare('narval_wrench_system')

        # Define default configuration paths
    default_config_path = PathJoinSubstitution([stonefish_share, 'config', 'windturbine_bluerov2.yaml'])
    default_rviz_config_path = PathJoinSubstitution([stonefish_share, 'rviz', 'tank_bluerov2_imu.rviz'])

        # Launch arguments
    config_arg = DeclareLaunchArgument(
        name="config",
        default_value=default_config_path,
        description="Path to the configuration file for the stonefish simulator"
    )
    rviz_config_arg = DeclareLaunchArgument(
        name="rviz_config",
        default_value=default_rviz_config_path,
        description="Path to the RViz2 configuration file"
    )

        # Nodes and launch inclusions
    thruster_manager_node = Node(
        package='narval_thruster_manager',
        executable="thruster_manager",
        parameters=[LaunchConfiguration('config')],
        output="screen"
    )

    narval_state_publisher_node = Node(
        package='narval_description',
        executable='narval_state_publisher',
        parameters=[LaunchConfiguration('config')]
    )

    wrench_system_launch = IncludeLaunchDescription(
        launch_description_source=PathJoinSubstitution([wrench_system_share, 'launch', 'base.launch.py']),
        launch_arguments={
            "config": LaunchConfiguration('config')
        }.items()
    )

    tf_imu = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        arguments=["0", "0", "0", "0", "0", "0", "base_link", "bluerov2/imu_filter"]
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', LaunchConfiguration('rviz_config')],
        output='screen'
    )

    # include another launch file
    launch_include = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(get_package_share_directory('stonefish_ros2') + \
                                      '/launch/stonefish_simulator.launch.py'),
        launch_arguments={
            'simulation_data': get_package_share_directory('narval_stonefish')+'/data/',
            'scenario_desc': get_package_share_directory('narval_stonefish')+'/scenarios/wreckage_bluerov2.scn',
            'simulation_rate': '30.0',
            'window_res_x': '1720',
            'window_res_y': '980',
            'rendering_quality': 'medium',
        }.items()
    )

        # Timed actions
    description_timer = TimerAction(period=1.0, actions=[narval_state_publisher_node])
    rviz_timer = TimerAction(period=1.0, actions=[rviz_node])
    stonefish_timer = TimerAction(period=2.0, actions=[launch_include])

    return LaunchDescription([
        config_arg,
        rviz_config_arg,
        stonefish_timer,
        thruster_manager_node,
        description_timer,
        wrench_system_launch,
        rviz_timer,
        tf_imu
    ])