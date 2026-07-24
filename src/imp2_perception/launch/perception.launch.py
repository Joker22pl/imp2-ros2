"""imp2_perception launch: ZED2i wrapper + RTAB-Map (visual SLAM).

ADR-0005: RTAB-Map as primary SLAM.
ADR-0004: ZED2i on Jetson Orin NX 16GB.
"""
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        # ZED2i camera wrapper
        Node(
            package='zed_wrapper',
            executable='zed_camera_node',
            name='zed2i',
            parameters=[{
                'general.camera_model': 'zed2i',
                'general.grab_resolution': 'HD720',
                'general.publish_rate': 30,
                'depth.depth_mode': 'NEURAL_PLUS',
                'pos_tracking.imu_fusion': True,
                'pos_tracking.publish_tf': True,
            }],
            output='screen',
        ),

        # RTAB-Map visual SLAM (initialization)
        Node(
            package='rtabmap_ros',
            executable='rtabmap',
            name='rtabmap',
            parameters=[{
                'frame_id': 'base_link',
                'subscribe_depth': True,
                'subscribe_rgb': True,
                'subscribe_odom_info': True,
                'Mem/ImageReindexing': True,
                'Mem/IncrementalMemory': True,
                'Mem/MemoryThr': 400,
            }],
            output='screen',
        ),
    ])
