"""micro-ROS agent launch (USB-CDC serial transport).

ADR-0002: USB-CDC serial as primary transport.
Latency: 1-5 ms, recovery < 2s, deterministic.
"""
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('port', default_value='/dev/ttyACM0'),
        DeclareLaunchArgument('baud', default_value='115200'),

        Node(
            package='micro_ros_agent',
            executable='micro_ros_agent',
            name='micro_ros_agent',
            arguments=[
                'serial',
                '--dev', LaunchConfiguration('port'),
                '-b', LaunchConfiguration('baud'),
                '-v6',
            ],
            output='screen',
        ),
    ])
