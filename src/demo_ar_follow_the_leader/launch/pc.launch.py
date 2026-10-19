import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
	ld = LaunchDescription()

	ld.add_action(Node(
		package='rviz2',
		executable='rviz2',
		arguments=[
			'-d',os.path.join(get_package_share_directory('demo_ar_follow_the_leader'), 'config', 'pc.rviz')
		],
		output='screen'
	))

	return ld