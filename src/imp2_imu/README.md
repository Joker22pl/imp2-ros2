# imp2_imu

BNO085 IMU driver for IMP2 robot (Hillcrest SH-2 fusion, 9-DOF).

**ADR-0012:** see `imp2-arch/adr/2026-07-24_imp2-adr-0012-imu-bno085.md`

## Adapted from Joker's imu_vector.py

Original (CircuitPython + ROS 1) → ROS 2 (rclpy) + Adafruit Blinka (CircuitPython-on-Linux).

### What changed

| Original | Adapted |
|---|---|
| `import rospy` | `import rclpy` + Node class |
| `bno.enable_feature(BNO_REPORT_ROTATION_VECTOR)` | also enables ACCELEROMETER, GYROSCOPE, MAGNETOMETER at configurable rates |
| `while True: print quaternion` | publish to `/imu/data` (sensor_msgs/Imu) at 200 Hz |
| ROS 1 (Float32) | ROS 2 (sensor_msgs/Imu, MagneticField, Temperature, QuaternionStamped) |
| `time.sleep(0.1)` | ROS 2 timers at configurable rates |

## Install on Jetson

```bash
# System deps for I2C
sudo apt install -y i2c-tools libi2c-dev

# Python deps (Adafruit Blinka = CircuitPython-on-Linux)
pip3 install --upgrade adafruit-blinka adafruit-circuitpython-bno08x

# Verify I2C sees BNO085
sudo i2cdetect -y 1    # should show 0x4A (default) or 0x4B
```

## I2C address

BNO085 default I2C address = `0x4A`. If conflict, change ADR-0012.

## Run

```bash
# Standalone
ros2 run imp2_imu imp2_imu_node

# Or via launch
ros2 launch imp2_imu imu.launch.py
```

## Topics

- `/imu/data` (sensor_msgs/Imu, 200 Hz, BEST_EFFORT)
- `/imu/mag` (sensor_msgs/MagneticField, 100 Hz, BEST_EFFORT)
- `/imu/rotation_vector` (QuaternionStamped, 200 Hz, debug)
- `/imu/temperature` (Temperature, 1 Hz; placeholder 25 °C)

## Frame

`imu_link` (REP-105, REP-103)

## Notes

- **Quaternion convention:** Adafruit BNO08x reports `(i, j, k, real)`; ROS uses `(x, y, z, w)`. We map directly.
- **Magnetic field units:** Adafruit reports µT; ROS uses Tesla. We convert `* 1e-6`.
- **Acceleration:** BNO08x `acceleration` = gravity + linear. If you want gravity-removed, enable `BNO_REPORT_LINEAR_ACCELERATION` instead.
- **Temperature:** BNO085 internal sensor — Adafruit driver does not expose it directly. Placeholder 25 °C for Phase 1.

## Files

- `imp2_imu/imp2_imu_node.py` — main driver (adapted from Joker's imu_vector.py)
- `launch/imu.launch.py` — launch file
- `package.xml` / `setup.py` — ROS 2 packaging

## Authors

- **Joker** — original `imu_vector.py` (Adafruit CircuitPython BNO08x + rospy)
- **Gaja** — adaptation to ROS 2 rclpy + Adafruit Blinka + multi-publisher pattern
