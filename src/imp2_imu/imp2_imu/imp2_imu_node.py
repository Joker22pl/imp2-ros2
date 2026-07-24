#!/usr/bin/env python3
"""
imp2_imu_node: BNO085 driver wrapper for ROS 2.

ADR-0012: BNO085 (Hillcrest SH-2) as primary IMU.

This is a SKELETON — adapted to integrate with Joker's existing BNO085 code.
Topics:
    /imu/data            sensor_msgs/Imu           200 Hz
    /imu/mag             sensor_msgs/MagneticField  100 Hz
    /imu/rotation_vector QuaternionStamped          200 Hz (debug)
    /imu/temperature     Temperature                 1 Hz

Frame: imu_link (REP-105, REP-103)

The actual sensor reading and fusion is delegated to Joker's BNO085 code.
Once provided, we'll integrate it into the _read_sensor() method below.

Authors: Joker (BNO085 code) + Gaja (ROS 2 wrapper)
License: MIT
"""

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy

from sensor_msgs.msg import Imu, MagneticField, Temperature
from geometry_msgs.msg import QuaternionStamped
from std_msgs.msg import Header

# TODO: import Joker's BNO085 code
# from bno08x_driver import BNO085  # or whatever Joker's module is called
# import smbus2  # for I2C


class Imp2ImuNode(Node):
    def __init__(self):
        super().__init__('imp2_imu')

        # Parameters
        self.declare_parameter('port', '/dev/i2c-1')  # Jetson I2C bus
        self.declare_parameter('i2c_address', 0x4A)
        self.declare_parameter('frame_id', 'imu_link')
        self.declare_parameter('pub_rate_hz', 200)
        self.declare_parameter('mag_rate_hz', 100)
        self.declare_parameter('temp_rate_hz', 1)

        port = self.get_parameter('port').value
        addr = self.get_parameter('i2c_address').value
        self.frame_id = self.get_parameter('frame_id').value
        pub_hz = self.get_parameter('pub_rate_hz').value

        # QoS: real-time, best-effort
        qos_sensor = QoSProfile(
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=1,
        )

        # Publishers
        self.pub_imu = self.create_publisher(Imu, '/imu/data', qos_sensor)
        self.pub_mag = self.create_publisher(MagneticField, '/imu/mag', qos_sensor)
        self.pub_rot = self.create_publisher(QuaternionStamped, '/imu/rotation_vector', qos_sensor)
        self.pub_temp = self.create_publisher(Temperature, '/imu/temperature', 10)

        # === INTEGRATION POINT ===
        # Initialize BNO085 here using Joker's code:
        # self.bno085 = BNO085(port, addr)
        # self.bno085.begin()
        # self.bno085.enable_rotation_vector(rate_hz=pub_hz)
        # self.bno085.enable_magnetometer(rate_hz=mag_rate_hz)
        # === END INTEGRATION POINT ===

        self.get_logger().info(f'imp2_imu node started (frame={self.frame_id}, rate={pub_hz} Hz)')
        self.get_logger().warn('SKELETON MODE — BNO085 not yet integrated. Awaiting Joker code.')

        # Timer for /imu/data and /imu/rotation_vector
        self.timer_imu = self.create_timer(1.0 / pub_hz, self.publish_imu)
        # Timer for /imu/mag (lower rate)
        self.timer_mag = self.create_timer(1.0 / self.get_parameter('mag_rate_hz').value, self.publish_mag)
        # Timer for /imu/temperature
        self.timer_temp = self.create_timer(1.0 / self.get_parameter('temp_rate_hz').value, self.publish_temp)

    def _read_sensor(self):
        """
        Read BNO085 sensor.

        TODO: Replace with Joker's BNO085 code.

        Returns:
            dict with keys:
                quaternion: (x, y, z, w) tuple
                angular_velocity: (x, y, z) rad/s tuple
                linear_acceleration: (x, y, z) m/s^2 tuple
                magnetic_field: (x, y, z) Tesla tuple
                temperature: float (Celsius)
            or None if no data.
        """
        # PLACEHOLDER — replace with real sensor read
        return None

    def _make_header(self):
        return Header(
            stamp=self.get_clock().now().to_msg(),
            frame_id=self.frame_id,
        )

    def publish_imu(self):
        data = self._read_sensor()
        if data is None:
            return  # No data yet (skeleton mode)

        # /imu/data
        imu_msg = Imu()
        imu_msg.header = self._make_header()
        imu_msg.orientation.x, imu_msg.orientation.y, imu_msg.orientation.z, imu_msg.orientation.w = data['quaternion']
        imu_msg.orientation_covariance = [0.01, 0, 0, 0, 0.01, 0, 0, 0, 0.01]  # diagonal
        imu_msg.angular_velocity.x, imu_msg.angular_velocity.y, imu_msg.angular_velocity.z = data['angular_velocity']
        imu_msg.angular_velocity_covariance = [0.01, 0, 0, 0, 0.01, 0, 0, 0, 0.01]
        imu_msg.linear_acceleration.x, imu_msg.linear_acceleration.y, imu_msg.linear_acceleration.z = data['linear_acceleration']
        imu_msg.linear_acceleration_covariance = [0.1, 0, 0, 0, 0.1, 0, 0, 0, 0.1]
        self.pub_imu.publish(imu_msg)

        # /imu/rotation_vector (debug)
        rot_msg = QuaternionStamped()
        rot_msg.header = self._make_header()
        rot_msg.quaternion = imu_msg.orientation
        self.pub_rot.publish(rot_msg)

    def publish_mag(self):
        data = self._read_sensor()
        if data is None:
            return
        mag_msg = MagneticField()
        mag_msg.header = self._make_header()
        mag_msg.magnetic_field.x, mag_msg.magnetic_field.y, mag_msg.magnetic_field.z = data['magnetic_field']
        mag_msg.magnetic_field_covariance = [0.01, 0, 0, 0, 0.01, 0, 0, 0, 0.01]
        self.pub_mag.publish(mag_msg)

    def publish_temp(self):
        data = self._read_sensor()
        if data is None:
            return
        temp_msg = Temperature()
        temp_msg.header = self._make_header()
        temp_msg.temperature = data['temperature']
        temp_msg.variance = 0.5
        self.pub_temp.publish(temp_msg)


def main(args=None):
    rclpy.init(args=args)
    node = Imp2ImuNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
