#!/usr/bin/env python3
"""imp2_safety: e-stop bridge.

ADR-0007: subscribes /emergency_stop topic, forwards to firmware via micro-ROS.

NOTE: This is a skeleton. Real implementation will need to send ESTOP to ESP32
via micro-ROS service call (imp2_msgs/srv/ResetEstop.srv is reserved for this).
"""
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy

from std_msgs.msg import Empty
from imp2_msgs.msg import EmergencyStop


class EstopBridgeNode(Node):
    def __init__(self):
        super().__init__('imp2_estop_bridge')

        # RELIABLE + TRANSIENT_LOCAL for safety messages
        qos_safety = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=1,
        )
        self.sub = self.create_subscription(
            EmergencyStop, '/emergency_stop', self.on_estop, qos_safety
        )
        self.get_logger().info('estop_bridge ready (subscribes /emergency_stop)')

    def on_estop(self, msg: EmergencyStop):
        self.get_logger().error(
            f'EMERGENCY STOP received: reason={msg.reason}, msg={msg.message.data!r}'
        )
        # TODO: forward to ESP32 via micro-ROS service call
        # For Phase 1, just log + (optionally) trigger motor_stop on Jetson side
        # via imp2_base node.


def main(args=None):
    rclpy.init(args=args)
    node = EstopBridgeNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
