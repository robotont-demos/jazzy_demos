#!/usr/bin/env python3

import rclpy
import numpy as np
from rclpy.node import Node
from geometry_msgs.msg import Twist
from tf_transformations import quaternion_matrix
from ros2_aruco_interfaces.msg import ArucoMarkers

MAX_LIN_VEL = 0.2
MAX_ANG_VEL = 0.2

GOAL_TOLERANCE = 0.1
ANGLE_TOLERANCE = 0.1
GOAL_DIST_FROM_MARKER = 0.5

def cam_to_ros(vec):
	return np.array([
	vec[2],		# forward/backward:	cam z
	-vec[0],	# left/right:		-cam x
	-vec[1],	# up/down:			-cam y
	])

def clip(val, min_val, max_val):
	return min(max(val, min_val), max_val)


class ArSteeringNode(Node):
	def __init__(self):
		super().__init__('ar_follow_the_leader')

		self.declare_parameter('marker_id', 0)
		self.declare_parameter('cmd_vel_topic', '/cmd_vel')

		self.marker_id = self.get_parameter('marker_id').value
		cmd_vel_topic = self.get_parameter('cmd_vel_topic').value

		self.get_logger().info(f"Marker ID: {self.marker_id}")
		self.get_logger().info(f"Velocity command topic: {cmd_vel_topic}")

		self.sub_poses = self.create_subscription(ArucoMarkers, '/aruco_markers', self.pose_callback, 1)
		self.pub_twist = self.create_publisher(Twist, cmd_vel_topic, 1)

	def pose_callback(self, msg):
		cmd = Twist()

		# Find the desired marker, otherwise publish ZERO speed
		if self.marker_id in msg.marker_ids:
			# self.get_logger().info(f"Found marker {self.marker_id}")

			marker_idx = msg.marker_ids.index(self.marker_id)
			pose = msg.poses[marker_idx]
			marker_position = np.array([
				pose.position.x,
				pose.position.y,
				pose.position.z,
				0])
			marker_orientation = (
				pose.orientation.x,
				pose.orientation.y,
				pose.orientation.z,
				pose.orientation.w
			) 

			# Start with a unit vector
			goal_dir = np.array([0, 0, 1, 0])
		
			# Rotation matrix that represents marker orientation
			rot_mat = quaternion_matrix(marker_orientation)
			# Rotate the unit vec so it points from the marker
			goal_dir = rot_mat.dot(goal_dir)
			# Snap unit vector to marker position facing away from it with magnitude GOAL_DIST_FROM_MARKER
			goal_pos = marker_position + (goal_dir * GOAL_DIST_FROM_MARKER)
			# Remap from camera/marker frame to ROS
			goal_pos = cam_to_ros(goal_pos[:3])
			marker_position_ros = cam_to_ros(marker_position[:3])

			# Find planar distance to the goal
			dist_to_goal = np.linalg.norm(goal_pos[0:2])
			dist_to_marker = np.linalg.norm(marker_position_ros[0:2])

			# Angle between robot's and marker's forward direction in robot's xy-plane
			angle = np.arctan2(marker_position_ros[1], marker_position_ros[0])

			# self.get_logger().info(f"Angle: {angle}")
			# self.get_logger().info(f"Dist to marker: {dist_to_marker}")

			if abs(angle) > ANGLE_TOLERANCE or dist_to_goal > GOAL_TOLERANCE:
				cmd.linear.x = clip(goal_pos[0], -MAX_LIN_VEL, MAX_LIN_VEL)
				cmd.linear.y = clip(goal_pos[1], -MAX_LIN_VEL, MAX_LIN_VEL)
				cmd.angular.z = clip(angle, -MAX_ANG_VEL, MAX_ANG_VEL)

		self.pub_twist.publish(cmd)


def main(args=None):
	rclpy.init(args=args)
	node = ArSteeringNode()
	rclpy.spin(node)
	node.destroy_node()
	rclpy.shutdown()


if __name__ == '__main__':
	main()
