# OTA status
std_msgs/Header header
uint8 state              # 0=idle, 1=checking, 2=downloading, 3=verifying, 4=installing, 5=rebooting, 6=success, 7=fail
string current_version
string target_version
uint8 progress_percent
string message
