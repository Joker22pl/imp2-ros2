"""imp2_safety launch: lifecycle + e-stop bridge + heartbeat monitor.

ADR-0007: ESP32 = owner of safety state.
heartbeat 50 Hz, timeout 200 ms.
"""
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        # E-stop bridge (subscribes /emergency_stop, publishes to firmware)
        Node(
            package='imp2_safety',
            executable='estop_bridge',
            name='imp2_estop_bridge',
            output='screen',
        ),

        # Heartbeat monitor (cross-checks ESP32 heartbeat vs ROS 2)
        Node(
            package='imp2_safety',
            executable='heartbeat_monitor',
            name='imp2_heartbeat_monitor',
            output='screen',
        ),

        # Safety state publisher (aggregates ROS 2 lifecycle)
        Node(
            package='imp2_safety',
            executable='safety_state',
            name='imp2_safety_state',
            output='screen',
        ),
    ])
