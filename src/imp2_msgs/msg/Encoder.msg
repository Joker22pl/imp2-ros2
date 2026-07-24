# Wheel encoder state (from ESP32)
std_msgs/Header header
uint32 ticks_left
uint32 ticks_right
float32 velocity_left    # m/s
float32 velocity_right   # m/s
uint8 estop_status       # 0=OK, 1=ESTOP, 2=FAULT
