#!/usr/bin/env python3
"""
imp2_imu_node: BNO085 driver for IMP2 robot (ROS 2).

ADR-0012: BNO085 (Hillcrest SH-2) as primary IMU.

Adapted from Joker's imu_vector.py (Adafruit CircuitPython BNO08x + rospy)
to ROS 2 (rclpy) + Adafruit Blinka (CircuitPython-on-Linux compatibility layer).

Differences from original:
  - rospy -> rclpy
  - Quaternion-only mode (per Joker's original code) PLUS accel/gyro/mag
  - Topics:
      /imu/data             sensor_msgs/Imu            200 Hz
      /imu/mag              sensor_msgs/MagneticField  100 Hz
      /imu/rotation_vector  QuaternionStamped           200 Hz (debug)
      /imu/temperature      Temperature                 1 Hz
  - Frame: imu_link (REP-105, REP-103)
  - BEST_EFFORT QoS (real-time)
  - Install: pip3 install adafruit-blinka adafruit-circuitpython-bno08x

Original code by Bryan Siepert (Adafruit), adapted by Gaja (architect) + Joker.
License: MIT
"""

import time
import struct

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy

from sensor_msgs.msg import Imu, MagneticField, Temperature
from geometry_msgs.msg import QuaternionStamped
from std_msgs.msg import Header

# Adafruit Blinka (CircuitPython-on-Linux) — gives us `board` and `busio`
# on a Jetson / Raspberry Pi / etc.
try:
    import board
    import busio
    from adafruit_bno08x import (
        BNO_REPORT_ACCELEROMETER,
        BNO_REPORT_GYROSCOPE,
        BNO_REPORT_MAGNETOMETER,
        BNO_REPORT_ROTATION_VECTOR,
    )
    from adafruit_bno08x.i2c import BNO08X_I2C
except ImportError as e:
    raise SystemExit(
        "Missing Adafruit Blinka + BNO08x libs. On Jetson:\n"
        "  pip3 install adafruit-blinka adafruit-circuitpython-bno08x\n"
        f"Original error: {e}"
    )


# === BNO08x report intervals (in microseconds, per Adafruit driver) ===
# Lower = faster rate. 5 ms = 200 Hz, 10 ms = 100 Hz, etc.
REPORT_INTERVAL_ROT_US = 5_000     # 200 Hz rotation vector
REPORT_INTERVAL_GYRO_US = 5_000    # 200 Hz gyro
REPORT_INTERVAL_ACCEL_US = 5_000   # 200 Hz accel
REPORT_INTERVAL_MAG_US = 10_000    # 100 Hz magnetometer


class Imp2ImuNode(Node):
    def __init__(self):
        super().__init__('imp2_imu')

        # === Parameters ===
        self.declare_parameter('i2c_frequency', 400_000)
        self.declare_parameter('frame_id', 'imu_link')
        self.declare_parameter('pub_rate_hz', 200.0)
        self.declare_parameter('mag_rate_hz', 100.0)
        self.declare_parameter('temp_rate_hz', 1.0)

        i2c_freq = self.get_parameter('i2c_frequency').value
        self.frame_id = self.get_parameter('frame_id').value
        self.pub_hz = float(self.get_parameter('pub_rate_hz').value)
        self.mag_hz = float(self.get_parameter('mag_rate_hz').value)
        self.temp_hz = float(self.get_parameter('temp_rate_hz').value)

        # === I2C + BNO085 init (from Joker's imu_vector.py) ===
        self.get_logger().info(f'Init BNO085 (I2C freq={i2c_freq} Hz)')
        self.i2c = busio.I2C(board.SCL, board.SDA, frequency=i2c_freq)
        self.bno = BNO08X_I2C(self.i2c)

        # Enable all 4 reports (rotation vector is the most important one,
        # which Joker's original code already used)
        self.bno.enable_feature(BNO_REPORT_ROTATION_VECTOR, REPORT_INTERVAL_ROT_US)
        self.bno.enable_feature(BNO_REPORT_GYROSCOPE,        REPORT_INTERVAL_GYRO_US)
        self.bno.enable_feature(BNO_REPORT_ACCELEROMETER,    REPORT_INTERVAL_ACCEL_US)
        self.bno.enable_feature(BNO_REPORT_MAGNETOMETER,     REPORT_INTERVAL_MAG_US)

        # === QoS: real-time, best-effort (sensor data) ===
        qos_sensor = QoSProfile(
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=1,
        )

        # === Publishers ===
        self.pub_imu = self.create_publisher(Imu, '/imu/data', qos_sensor)
        self.pub_mag = self.create_publisher(MagneticField, '/imu/mag', qos_sensor)
        self.pub_rot = self.create_publisher(QuaternionStamped, '/imu/rotation_vector', qos_sensor)
        self.pub_temp = self.create_publisher(Temperature, '/imu/temperature', 10)

        # === Covariance values (diagonal, std_dev^2) ===
        # Rotation vector accuracy from BNO085 datasheet: ~1.8 deg = 0.0314 rad
        # → variance 0.001 rad^2
        # Accel noise: ~0.05 m/s^2 → variance 0.0025
        # Gyro noise:  ~0.005 rad/s → variance 2.5e-5
        # Mag noise:   ~1.0 uT    → variance 1.0 (T^2)
        self.ORI_COV = 0.01
        self.GYRO_COV = 0.0025
        self.ACCEL_COV = 0.05

        # === Timers ===
        # /imu/data and /imu/rotation_vector at pub_hz
        self.timer_imu = self.create_timer(1.0 / self.pub_hz, self.publish_imu)
        # /imu/mag at mag_hz (lower rate, less bandwidth)
        self.timer_mag = self.create_timer(1.0 / self.mag_hz, self.publish_mag)
        # /imu/temperature at temp_hz (BNO085 has internal temp sensor)
        self.timer_temp = self.create_timer(1.0 / self.temp_hz, self.publish_temp)

        self.get_logger().info(
            f'imp2_imu ready: imu={self.pub_hz} Hz, mag={self.mag_hz} Hz, '
            f'temp={self.temp_hz} Hz, frame={self.frame_id}'
        )

    def _make_header(self):
        return Header(
            stamp=self.get_clock().now().to_msg(),
            frame_id=self.frame_id,
        )

    def _build_covariance_diagonal(self, var):
        """Return a 9-element list (3x3 row-major) for a 3x3 covariance matrix
        with `var` on the diagonal and 0 elsewhere."""
        return [var if i == j else 0.0 for i in range(3) for j in range(3)]

    def publish_imu(self):
        """Publish /imu/data (orientation + ang_vel + lin_accel) and
        /imu/rotation_vector (debug)."""
        try:
            quat_i, quat_j, quat_k, quat_real = self.bno.quaternion
            gyro_x, gyro_y, gyro_z = self.bno.gyro
            accel_x, accel_y, accel_z = self.bno.acceleration
        except Exception as e:
            self.get_logger().warn(f'BNO085 read error (imu): {e}')
            return

        # === /imu/data ===
        msg = Imu()
        msg.header = self._make_header()
        # BNO085 quaternion: (i, j, k, real) → ROS uses (x, y, z, w)
        msg.orientation.x = float(quat_i)
        msg.orientation.y = float(quat_j)
        msg.orientation.z = float(quat_k)
        msg.orientation.w = float(quat_real)
        msg.orientation_covariance = self._build_covariance_diagonal(self.ORI_COV)

        # Gyro is in rad/s already (per Adafruit BNO08x docs)
        msg.angular_velocity.x = float(gyro_x)
        msg.angular_velocity.y = float(gyro_y)
        msg.angular_velocity.z = float(gyro_z)
        msg.angular_velocity_covariance = self._build_covariance_diagonal(self.GYRO_COV)

        # Accel is in m/s^2 (gravity included — BNO085 reports "acceleration" = gravity + linear)
        # If we want gravity-removed, use BNO_REPORT_LINEAR_ACCELERATION instead.
        msg.linear_acceleration.x = float(accel_x)
        msg.linear_acceleration.y = float(accel_y)
        msg.linear_acceleration.z = float(accel_z)
        msg.linear_acceleration_covariance = self._build_covariance_diagonal(self.ACCEL_COV)

        self.pub_imu.publish(msg)

        # === /imu/rotation_vector (debug) ===
        rot = QuaternionStamped()
        rot.header = msg.header
        rot.quaternion = msg.orientation
        self.pub_rot.publish(rot)

    def publish_mag(self):
        """Publish /imu/mag (magnetic field in Tesla)."""
        try:
            mag_x, mag_y, mag_z = self.bno.magnetic
        except Exception as e:
            self.get_logger().warn(f'BNO085 read error (mag): {e}')
            return

        # Adafruit reports mag in µT; ROS uses Tesla.
        # 1 µT = 1e-6 T
        msg = MagneticField()
        msg.header = self._make_header()
        msg.magnetic_field.x = float(mag_x) * 1e-6
        msg.magnetic_field.y = float(mag_y) * 1e-6
        msg.magnetic_field.z = float(mag_z) * 1e-6
        msg.magnetic_field_covariance = self._build_covariance_diagonal(1e-2)  # 0.1 µT std
        self.pub_mag.publish(msg)

    def publish_temp(self):
        """Publish /imu/temperature. BNO085 has an internal temp sensor.
        We approximate it from the chip — note: the Adafruit driver does not
        directly expose a temperature property, so this is a placeholder.

        If you need accurate temp, the BNO08x SHTP protocol has a
        'temperature' report (0x0E). For Phase 1 we publish 25 °C (ambient)
        as a safe default; can be extended later."""
        msg = Temperature()
        msg.header = self._make_header()
        msg.temperature = 25.0
        msg.variance = 5.0
        self.pub_temp.publish(msg)


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
