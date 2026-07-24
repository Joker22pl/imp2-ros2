# Battery status (from ESP32 ADC)
std_msgs/Header header
float32 voltage_v
float32 current_a
float32 capacity_percent
uint8 health             # 0=good, 1=warning, 2=critical
