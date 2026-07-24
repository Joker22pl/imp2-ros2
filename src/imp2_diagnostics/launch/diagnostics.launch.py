"""imp2_diagnostics launch: diagnostic_aggregator + watchers."""
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='diagnostic_aggregator',
            executable='aggregator_node',
            name='imp2_diag_aggregator',
            output='screen',
        ),
        Node(
            package='imp2_diagnostics',
            executable='battery_monitor',
            name='imp2_battery_monitor',
            output='screen',
        ),
        Node(
            package='imp2_diagnostics',
            executable='cpu_temp_monitor',
            name='imp2_cpu_temp_monitor',
            output='screen',
        ),
    ])
