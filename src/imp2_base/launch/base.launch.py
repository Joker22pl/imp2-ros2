"""imp2_base launch: ros2_control + diff_drive_controller.

ADR-0006: encoders (Pololu 64 CPR + EKF deadband).
ADR-0003: motor current limit.
"""
from launch import LaunchDescription
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():
    return LaunchDescription([
        # Controller manager
        Node(
            package='controller_manager',
            executable='ros2_control_node',
            parameters=[{'robot_description': ''}],
            output='screen',
        ),

        # Diff drive controller
        Node(
            package='controller_manager',
            executable='spawner',
            arguments=['diff_drive_controller', '--controller-manager', '/controller_manager'],
        ),

        # Joint state broadcaster
        Node(
            package='controller_manager',
            executable='spawner',
            arguments=['joint_state_broadcaster', '--controller-manager', '/controller_manager'],
        ),
    ])
