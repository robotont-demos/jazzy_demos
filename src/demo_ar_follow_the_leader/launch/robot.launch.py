from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node


def robot_topic_create(robot_id, topic):
	return PythonExpression(["'/rt' + '", robot_id, "' + '/" + topic + "'"])


def generate_launch_description():
	ld = LaunchDescription()

	# Arguments
	ld.add_action(DeclareLaunchArgument(
		'robot_id',
		default_value='0',
		description='used for image_topic (/rtXX/camera/image_raw), camera_info_topic (/rtXX/camera/camera_info) and cmd_vel_topic (/rtXX/cmd_vel)'
	))

	ld.add_action(DeclareLaunchArgument(
		'marker_id',
		default_value='0',
		description='ArUco marker ID to follow'
	))

	ld.add_action(DeclareLaunchArgument(
			'marker_size',
			default_value='0.0625',
			description='ArUco marker size in meters'
	))

	# Nodes
	ld.add_action(Node(
		package='ros2_aruco',
		executable='aruco_node',
		parameters=[{
			'image_topic': robot_topic_create(LaunchConfiguration('robot_id'), 'camera/image_raw'),
			'camera_info_topic': robot_topic_create(LaunchConfiguration('robot_id'), 'camera/camera_info')
			}]
	))

	ld.add_action(Node(
		package='demo_ar_follow_the_leader',
		executable='ar_follow_the_leader.py',
		parameters=[{
			'marker_id': LaunchConfiguration('marker_id'),
			'cmd_vel_topic': robot_topic_create(LaunchConfiguration('robot_id'), 'cmd_vel')
		}]
	))

	return ld