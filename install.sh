#!/usr/bin/env bash
# IMP2 ROS 2 install — Phase 1 (Phase 1: skeleton only)
set -euo pipefail

ROS_DISTRO=${ROS_DISTRO:-humble}
WORKSPACE_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "==> IMP2 ROS 2 install (Phase 1 skeleton)"
echo "    ROS_DISTRO: $ROS_DISTRO"
echo "    WORKSPACE:  $WORKSPACE_DIR"

# Source ROS 2
if [ -f "/opt/ros/${ROS_DISTRO}/setup.bash" ]; then
    source "/opt/ros/${ROS_DISTRO}/setup.bash"
    echo "==> ROS 2 sourced from /opt/ros/${ROS_DISTRO}"
else
    echo "ERROR: ROS 2 ${ROS_DISTRO} not found. Install with:"
    echo "    sudo apt install ros-${ROS_DISTRO}-desktop"
    exit 1
fi

# Install dependencies (rosdep)
echo "==> Installing dependencies via rosdep"
if [ -f "src/imp2_msgs/package.xml" ]; then
    sudo apt-get update -q
    sudo rosdep init || true
    rosdep update --rosdistro=$ROS_DISTRO
    rosdep install --from-paths src --ignore-src -r -y --rosdistro=$ROS_DISTRO
fi

# Build workspace
echo "==> Building workspace"
cd "$WORKSPACE_DIR"
colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release

echo "==> Done. Source: source ${WORKSPACE_DIR}/install/setup.bash"
