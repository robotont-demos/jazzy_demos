from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node


def generate_launch_description():
	ld = LaunchDescription()

	rt_number_arg = DeclareLaunchArgument(
		'rt_number',
		default_value='0',
		description='Robotont number (for example 50). Used for: camera topic (/rtXX/camera/...) and marker id'
	)

	# Runs by default on Robotont 3 Lite
	# ld.add_action(Node(
	# 	package='usb_cam',
	# 	executable='usb_cam_node_exe',
	# ))

	ld.add_action(Node(
		package='ros2_aruco',
		executable='aruco_node',
		parameters=[{
			'image_topic': ['/rt', rt_number, '/camera/image_raw'],
			'camera_info_topic': ['/rt', rt_number, '/camera/camera_info']
			}]
	))

	ld.add_action(Node(
		package='demo_ar_follow_the_leader',
		executable='ar_follow_the_leader.py'
	))

	return ld