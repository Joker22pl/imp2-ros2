"""imp2_imu launch: BNO085 IMU node.

ADR-0012: BNO085 over I2C Qwiic to reComputer J4012.
Frame: imu_link (10 cm above base_link, per URDF + ADR-0008).
"""
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('i2c_frequency', default_value='400000'),
        DeclareLaunchArgument('frame_id', default_value='imu_link'),
        DeclareLaunchArgument('pub_rate_hz', default_value='200.0'),
        DeclareLaunchArgument('mag_rate_hz', default_value='100.0'),
        DeclareLaunchArgument('temp_rate_hz', default_value='1.0'),

        Node(
            package='imp2_imu',
            executable='imp2_imu_node',
            name='imp2_imu',
            parameters=[{
                'i2c_frequency': LaunchConfiguration('i2c_frequency'),
                'frame_id': LaunchConfiguration('frame_id'),
                'pub_rate_hz': LaunchConfiguration('pub_rate_hz'),
                'mag_rate_hz': LaunchConfiguration('mag_rate_hz'),
                'temp_rate_hz': LaunchConfiguration('temp_rate_hz'),
            }],
            output='screen',
        ),
    ])
