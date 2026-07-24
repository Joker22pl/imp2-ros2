# imp2_bringup

Main launch files + systemd units for IMP2 robot.

## Usage

```bash
# Standard
ros2 launch imp2_bringup imp2.launch.py

# Without nav (teleop only)
ros2 launch imp2_bringup imp2.launch.py use_nav:=false

# Simulation
ros2 launch imp2_bringup imp2.launch.py use_sim:=true
```

## Files

- `launch/imp2.launch.py` — main launch
- `config/imp2_bringup.yaml` — global config
- `systemd/imp2.service` — systemd unit for auto-start

## Phase 1 (current)

- [x] launch file structure
- [x] packaging metadata
- [ ] E-stop wiring (depends on ADR-0007 hardware)
- [ ] Docker compose for Jetson
