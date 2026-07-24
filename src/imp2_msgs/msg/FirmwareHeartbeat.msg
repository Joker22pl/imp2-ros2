# Firmware heartbeat (50 Hz)
std_msgs/Header header
uint32 sequence
uint32 uptime_s
uint8 firmware_state     # 0=BOOT, 1=IDLE, 2=READY, 3=ACTIVE, 4=STOPPING, 5=FAULT, 6=ESTOP, 7=DISCONNECTED
float32 battery_voltage_v
float32 cpu_temp_c
uint32 watchdog_kicks
uint32 heartbeat_last_rx_ms
string last_error
