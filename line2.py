#!/usr/bin/env python

import rospy
from mavros_msgs.msg import CommandLong

rospy.init_node('set_yaw_angle')

# Set up a publisher to send the command to the drone
cmd_pub = rospy.Publisher('/mavros/cmd/command', CommandLong, queue_size=10)

# Define the message that sets the yaw angle
cmd_msg = CommandLong()
cmd_msg.command = 3000 # MAV_CMD_CONDITION_YAW
cmd_msg.param1 = 0.0 # Yaw angle (radians)
cmd_msg.param2 = 1.0 # Yaw rate (radians/second)
cmd_msg.param3 = 1 # Direction: 1=Clockwise, -1=Counter-clockwise
cmd_msg.param4 = 0.0 # Relative offset (radians)
cmd_msg.param5 = 0.0 # Final angle (radians)
cmd_msg.param6 = 0.0 # Hold time (seconds)
cmd_msg.param7 = 0.0 # Unused parameter

# Publish the command
cmd_pub.publish(cmd_msg)

rospy.spin()
