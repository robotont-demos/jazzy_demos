cmake_minimum_required(VERSION 3.8)
project(demo_ar_follow_the_leader)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()


# find dependencies
find_package(ament_cmake_python REQUIRED)

find_package(rclpy REQUIRED)
find_package(geometry_msgs REQUIRED)

# Python nodes
ament_python_install_package(${PROJECT_NAME})

install(PROGRAMS
  scripts/ar_follow_the_leader.py
  DESTINATION lib/${PROJECT_NAME}
)

# Launch files
install(DIRECTORY
  launch config
  DESTINATION share/${PROJECT_NAME}/
)


ament_package()
