#!/usr/bin/env python3
"""imp2_safety: heartbeat monitor.

ADR-0007: cross-checks ESP32 /firmware/heartbeat vs ROS 2 system state.

NOTE: skeleton — full EKF + watchdog not yet implemented.
"""
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy

from imp2_msgs.msg import FirmwareHeartbeat


HEARTBEAT_TIMEOUT_MS = 200  # ADR-0007


class HeartbeatMonitorNode(Node):
    def __init__(self):
        super().__init__('imp2_heartbeat_monitor')

        qos = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=10,
        )
        self.sub = self.create_subscription(
            FirmwareHeartbeat, '/firmware/heartbeat', self.on_hb, qos
        )
        self.get_logger().info(f'heartbeat_monitor ready (timeout={HEARTBEAT_TIMEOUT_MS} ms)')

    def on_hb(self, msg: FirmwareHeartbeat):
        # TODO: maintain rolling window of last N heartbeats, check firmware_state
        # transitions, alarm on FAULT/ESTOP/DISCONNECTED, trigger emergency_stop if
        # heartbeat age > HEARTBEAT_TIMEOUT_MS.
        self.get_logger().debug(
            f'heartbeat seq={msg.sequence} state={msg.firmware_state} '
            f'V={msg.battery_voltage_v:.2f} age={msg.heartbeat_last_rx_ms} ms'
        )


def main(args=None):
    rclpy.init(args=args)
    node = HeartbeatMonitorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
