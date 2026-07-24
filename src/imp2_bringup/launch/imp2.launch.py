"""Main launch file for IMP2 robot.

Launches all required nodes:
- Robot state publisher (URDF)
- micro-ROS agent
- imp2_base (diff_drive controller)
- imp2_perception (ZED2i)
- imp2_navigation (RTAB-Map + Nav2)
- imp2_teleop (joystick)
- imp2_diagnostics (aggregator)
- imp2_safety (lifecycle + e-stop)

Adrs referenced:
- ADR-0002 (transport USB-CDC)
- ADR-0005 (SLAM RTAB-Map)
- ADR-0007 (safety state machine)
- ADR-0011 (ROS 2 Humble)
"""
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    # Args
    use_sim = LaunchConfiguration('use_sim', default='false')
    use_nav = LaunchConfiguration('use_nav', default='true')
    use_teleop = LaunchConfiguration('use_teleop', default='true')

    # URDF
    urdf_file = os.path.join(
        get_package_share_directory('imp2_description'),
        'urdf', 'imp2.xacro'
    )
    robot_description = Command(['xacro ', urdf_file])

    # Nodes
    nodes = [
        # Robot state publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            parameters=[{'robot_description': robot_description}],
            output='screen',
        ),
        # micro-ROS agent (USB-CDC serial)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory('imp2_micro_ros_agent'),
                             'launch', 'agent_serial.launch.py')
            ),
        ),
        # imp2_base (ros2_control + diff_drive)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory('imp2_base'),
                             'launch', 'base.launch.py')
            ),
        ),
        # imp2_perception (ZED2i)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory('imp2_perception'),
                             'launch', 'perception.launch.py')
            ),
        ),
        # imp2_safety (lifecycle + e-stop)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory('imp2_safety'),
                             'launch', 'safety.launch.py')
            ),
        ),
        # imp2_diagnostics
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory('imp2_diagnostics'),
                             'launch', 'diagnostics.launch.py')
            ),
        ),
        # imp2_navigation (RTAB-Map + Nav2)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory('imp2_navigation'),
                             'launch', 'navigation.launch.py')
            ),
            condition=IfCondition(use_nav),
        ),
        # imp2_teleop
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory('imp2_teleop'),
                             'launch', 'teleop.launch.py')
            ),
            condition=IfCondition(use_teleop),
        ),
    ]

    return LaunchDescription(
        [DeclareLaunchArgument('use_sim', default_value='false'),
         DeclareLaunchArgument('use_nav', default_value='true'),
         DeclareLaunchArgument('use_teleop', default_value='true')]
        + nodes
    )
