# imp2_msgs

Custom message types for IMP2 robot.

## Messages

| Name | Purpose | Publisher | Subscriber |
|---|---|---|---|
| `Encoder.msg` | Wheel encoder ticks + velocity | ESP32 | imp2_base |
| `MotorState.msg` | PWM + current + temp per motor | ESP32 | imp2_diagnostics |
| `FirmwareHeartbeat.msg` | 50 Hz heartbeat from ESP32 | ESP32 | imp2_safety |
| `EmergencyStop.msg` | Soft E-stop trigger | operator | imp2_safety → ESP32 |
| `OtaStatus.msg` | OTA progress + state | ESP32 / imp2_bringup | operator |
| `BatteryStatus.msg` | voltage, current, % | ESP32 | imp2_diagnostics |

## Services

- `ResetEstop.srv` — manual reset from ESTOP/FAULT state
- `TriggerOta.srv` — trigger OTA check with target version

## Usage

```python
from imp2_msgs.msg import Encoder, FirmwareHeartbeat
from imp2_msgs.srv import ResetEstop
```

Generated headers available after `colcon build`.
