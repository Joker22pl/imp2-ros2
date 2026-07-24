#!/usr/bin/env python3
"""imp2_diagnostics: battery monitor.

ADR-0003: monitors LiFePO4 12V battery via imp2_msgs/BatteryStatus.

NOTE: skeleton — in Phase 1, the battery voltage is published by the ESP32
firmware (imp2_micro_ros) using ADC measurements on a voltage divider. This
node consumes that data, applies thresholds, and republishes to /diagnostics.

Wired from: imp2_msgs/BatteryStatus (from ESP32 firmware)
Publishes:  /diagnostics (level WARN when V < 11.5V, ERROR when V < 11.0V)
"""
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy

from imp2_msgs.msg import BatteryStatus
from diagnostic_msgs.msg import DiagnosticArray, DiagnosticStatus, KeyValue


# Per ADR-0003: thresholds for LiFePO4 4S 12V
WARN_V = 11.5   # WARN below this
ERROR_V = 11.0  # ERROR below this (autonomous safe-stop)


class BatteryMonitorNode(Node):
    def __init__(self):
        super().__init__('imp2_battery_monitor')

        qos = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=5,
        )
        self.sub = self.create_subscription(
            BatteryStatus, '/battery_state', self.on_battery, qos
        )
        self.pub = self.create_publisher(DiagnosticArray, '/diagnostics', 10)
        self.get_logger().info(
            f'battery_monitor ready (WARN<{WARN_V}V ERROR<{ERROR_V}V)'
        )

    def on_battery(self, msg: BatteryStatus):
        if msg.voltage_v < ERROR_V:
            level, name = DiagnosticStatus.ERROR, 'battery_critical'
            message = f'battery {msg.voltage_v:.2f}V < {ERROR_V}V threshold'
        elif msg.voltage_v < WARN_V:
            level, name = DiagnosticStatus.WARN, 'battery_low'
            message = f'battery {msg.voltage_v:.2f}V < {WARN_V}V threshold'
        else:
            level, name = DiagnosticStatus.OK, 'battery'
            message = f'battery {msg.voltage_v:.2f}V OK'

        status = DiagnosticStatus()
        status.level = level
        status.name = name
        status.message = message
        status.values = [
            KeyValue(key='voltage_v', value=f'{msg.voltage_v:.2f}'),
            KeyValue(key='current_a', value=f'{msg.current_a:.2f}'),
            KeyValue(key='capacity_percent', value=f'{msg.capacity_percent:.1f}'),
            KeyValue(key='health', value=str(msg.health)),
        ]

        arr = DiagnosticArray()
        arr.header.stamp = msg.header.stamp
        arr.status.append(status)
        self.pub.publish(arr)


def main(args=None):
    rclpy.init(args=args)
    node = BatteryMonitorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
