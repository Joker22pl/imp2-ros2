#!/usr/bin/env python3
"""imp2_safety: safety state aggregator.

ADR-0007: aggregates firmware state, heartbeat health, E-stop status.
Publishes a /diagnostics topic for the diagnostic_aggregator.
"""
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy

from diagnostic_msgs.msg import DiagnosticArray, DiagnosticStatus, KeyValue


class SafetyStateNode(Node):
    def __init__(self):
        super().__init__('imp2_safety_state')
        # TODO: subscribe to firmware/heartbeat, /emergency_stop, etc.
        # Aggregate into DiagnosticStatus and publish on /diagnostics.
        self.pub = self.create_publisher(DiagnosticArray, '/diagnostics', 10)
        self.get_logger().info('safety_state ready (publishes /diagnostics)')

    def publish_diag(self, level, name, message, values=None):
        status = DiagnosticStatus()
        status.level = level  # 0=OK, 1=WARN, 2=ERROR, 3=STALE
        status.name = name
        status.message = message
        if values:
            status.values = [
                KeyValue(key=k, value=str(v)) for k, v in values.items()
            ]
        arr = DiagnosticArray()
        arr.status.append(status)
        self.pub.publish(arr)


def main(args=None):
    rclpy.init(args=args)
    node = SafetyStateNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
