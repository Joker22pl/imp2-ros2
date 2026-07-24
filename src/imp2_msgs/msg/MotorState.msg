# Motor state (from ESP32)
std_msgs/Header header
uint8 motor_id           # 0=left, 1=right
uint8 pwm_duty           # 0-255
float32 current_amps
float32 temperature_c
uint8 state              # 0=off, 1=on, 2=brake, 3=estop
