# Soft E-stop trigger
std_msgs/Header header
uint8 reason             # 0=operator, 1=safety_node, 2=watchdog, 3=comms_lost
string message
