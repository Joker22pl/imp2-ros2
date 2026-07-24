# imp2_imu

BNO085 IMU driver (Hillcrest SH-2 fusion, 9-DOF).

**ADR-0012:** see `imp2-arch/adr/2026-07-24_imp2-adr-0012-imu-bno085.md`

**Status:** SKELETON — awaiting Joker's BNO085 code integration.

## Integration steps

1. Copy Joker's BNO085 code (vector display) into this package.
2. Replace the `_read_sensor()` method in `imp2_imu_node.py` with a call to the BNO085 library.
3. Update `setup.py` to include the BNO085 library as a dependency.
4. Test on real hardware.

## Topics

- `/imu/data` (sensor_msgs/Imu, 200 Hz)
- `/imu/mag` (sensor_msgs/MagneticField, 100 Hz)
- `/imu/rotation_vector` (QuaternionStamped, 200 Hz, debug)
- `/imu/temperature` (Temperature, 1 Hz)

## Frame

`imu_link` (REP-105, REP-103)
