cmake_minimum_required(VERSION 3.16)
project(imp2_msgs VERSION 0.1.0)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/Encoder.msg"
  "msg/MotorState.msg"
  "msg/FirmwareHeartbeat.msg"
  "msg/EmergencyStop.msg"
  "msg/OtaStatus.msg"
  "msg/BatteryStatus.msg"
  "srv/ResetEstop.srv"
  "srv/TriggerOta.srv"
)

ament_package()
