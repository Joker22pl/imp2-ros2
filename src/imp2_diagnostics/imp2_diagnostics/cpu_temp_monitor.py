#!/usr/bin/env python3
"""imp2_diagnostics: CPU temperature monitor (Jetson).

NOTE: skeleton — uses psutil for CPU temp on standard Linux, falls back
to vcgencmd for Raspberry Pi. On Jetson, /sys/devices/virtual/thermal/
has zone0 (CPU), zone1 (GPU), etc.
"""
import rclpy
from rclpy.node import Node

from diagnostic_msgs.msg import DiagnosticArray, DiagnosticStatus, KeyValue


class CpuTempMonitorNode(Node):
    def __init__(self):
        super().__init__('imp2_cpu_temp_monitor')
        self.pub = self.create_publisher(DiagnosticArray, '/diagnostics', 10)
        self.get_logger().info('cpu_temp_monitor ready')

        # Periodic publish (1 Hz)
        self.timer = self.create_timer(1.0, self.publish_temp)

    def _read_temp_c(self) -> float:
        """Read CPU temp from thermal zone 0 (Jetson convention)."""
        try:
            with open('/sys/devices/virtual/thermal/thermal_zone0/temp', 'r') as f:
                return int(f.read().strip()) / 1000.0  # m°C to °C
        except (FileNotFoundError, ValueError, OSError):
            return float('nan')

    def publish_temp(self):
        temp = self._read_temp_c()
        if temp != temp:  # NaN
            return
        if temp > 85.0:
            level = DiagnosticStatus.ERROR
            message = f'CPU {temp:.1f}°C > 85°C critical'
        elif temp > 75.0:
            level = DiagnosticStatus.WARN
            message = f'CPU {temp:.1f}°C > 75°C warm'
        else:
            level = DiagnosticStatus.OK
            message = f'CPU {temp:.1f}°C OK'

        status = DiagnosticStatus()
        status.level = level
        status.name = 'cpu_temp'
        status.message = message
        status.values = [KeyValue(key='temp_c', value=f'{temp:.1f}')]

        arr = DiagnosticArray()
        arr.status.append(status)
        self.pub.publish(arr)


def main(args=None):
    rclpy.init(args=args)
    node = CpuTempMonitorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
