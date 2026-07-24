# IMP2 — ROS 2 Workspace

ROS 2 (Humble) workspace dla robota IMP2. Zawiera 11 pakietów zgodnie z review v0.2 architektury.

**Status:** skeleton (Phase 1 — package structure + minimal content)
**Pliki:** wszystkie pakiety mają `package.xml`, `setup.py`/`CMakeLists.txt`, README, launch + config dir.

## Architektura

![C4 Context](https://placeholder-for-future-c4-diagram)

## Repozytoria

- [`imp2-arch`](../imp2-arch) — architektura (ADR-y, review, diagramy)
- [`imp2-ros2`](../imp2-ros2) — to repo (kod ROS 2)
- [`imp2-firmware`](../imp2-firmware) — firmware ESP32-S3 (ESP-IDF)

## Pakiety

| Pakiet | Cel | Faza |
|---|---|---|
| `imp2_bringup` | launch files + systemd | 1 |
| `imp2_description` | URDF/xacro + mesh | 1 |
| `imp2_base` | ros2_control + diff_drive | 1 |
| `imp2_micro_ros_agent` | agent config | 1 |
| `imp2_perception` | ZED2i wrappers | 1 |
| `imp2_navigation` | Nav2 config + RTAB-Map | 1 |
| `imp2_teleop` | joystick, keyboard | 1 |
| `imp2_diagnostics` | diagnostic_aggregator | 1 |
| `imp2_safety` | e-stop bridge + lifecycle | 1 |
| `imp2_ai` | LLM client (Phase 3) | 3 |
| `imp2_msgs` | custom message types | 1 |

## Quick Start

```bash
# Setup
cd imp2-ros2
./install.sh

# Build
colcon build --symlink-install

# Run
source install/setup.bash
ros2 launch imp2_bringup imp2.launch.py
```

## Zależności

- ROS 2 Humble (Ubuntu 22.04, ARM64 na Jetson)
- Docker (opcja)
- ZED SDK 5.x
- micro-ROS agent
- RTAB-Map + rtabmap_ros
- Nav2

## Dokumentacja

- `imp2-arch/00_inbox/2026-07-24_imp2-architecture-review-v0.2.md` — krytyczny review
- `imp2-arch/adr/` — Architecture Decision Records (8+ ADR-ów)
- `imp2-arch/12_Roadmap/12.1_Releases.md` — plan wersji (TODO)

## Owner

- **Joker** — project owner
- **Gaja** — architect, code review
