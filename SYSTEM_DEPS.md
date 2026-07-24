# imp2-ros2 — System dependencies (apt)

Some packages this workspace depends on are **not** part of the
workspace — they must be installed via apt. Run this **before**
`colcon build`:

```bash
sudo apt update
sudo apt install -y \
    ros-humble-ros-base \
    ros-humble-ros2-control \
    ros-humble-ros2-controllers \
    ros-humble-diff-drive-controller \
    ros-humble-nav2-bringup \
    ros-humble-nav2-common \
    ros-humble-robot-state-publisher \
    ros-humble-xacro \
    ros-humble-joint-state-publisher \
    ros-humble-teleop-twist-joy \
    ros-humble-teleop-twist-keyboard \
    ros-humble-joy \
    ros-humble-diagnostic-aggregator \
    ros-humble-rmw-cyclonedds-cpp \
    ros-humble-rtabmap \
    ros-humble-rtabmap-ros \
    ros-humble-robot-localization

# Stereolabs ZED SDK 5.x + ROS 2 wrapper
# See: https://www.stereolabs.com/docs/ros2/
# (download .run installer from stereolabs.com)

# Adafruit Blinka (CircuitPython-on-Linux) + BNO08x for imp2_imu
pip3 install --upgrade adafruit-blinka adafruit-circuitpython-bno08x
```

## Why these are external

- **ros2_control, diff-drive-controller, Nav2, RTAB-Map, robot-localization** —
  upstream Apache 2 / BSD ROS packages; not part of our workspace.
- **ZED SDK + zed-ros2-wrapper** — proprietary (Stereolabs); install per their docs.
- **Adafruit Blinka / BNO08x** — install via pip3 (Joker's code is adapted to Blinka
  for Linux; original was CircuitPython for microcontrollers).
- **micro-ros-agent** — Docker image `microros/micro-ros-agent:humble`.

## Phase 1 apt deps are minimal

- For Phase 1 (teleop only), you only need: `ros-humble-ros-base`, `ros-humble-joy`,
  `ros-humble-teleop-twist-joy`, `ros-humble-robot-state-publisher`,
  `ros-humble-xacro`, `ros-humble-rmw-cyclonedds-cpp`.
- Add Nav2 / RTAB-Map / ZED only when their packages are wired (Phase 1.5+).
