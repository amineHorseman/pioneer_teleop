#!/usr/bin/env python
####################################################### 
##             bendahmane.amine@gmail.com            ##
##            last update : Jan 31st, 2016           ##
#######################################################
## Description : This program take transforms simple ##
##  command line arguments (forward, backward, left, ## 
##	  right) to velocity commands. (by default, the  ##
## 	    robot moves for 1.5 seconds only)            ##
#######################################################

# configuration :
MAX_SPEED = 0.4
DEFAULT_MOVE_TIME = 1.5

#######################################################
##      DO NOT CHANGE ANYTHING AFTER THIS LINE!      ##
#######################################################

import rospy
import roslib; roslib.load_manifest('pioneer_teleop')
import sys
import time
from geometry_msgs.msg import Twist

rospy.init_node('commandline_teleop')

# read arguments :
direction = sys.argv[1]
if (direction != "forward") and (direction != "backward") and (direction != "right") and (direction != "left"):
	print " - Error : incorrect direction " + direction
	exit()


if (len(sys.argv) > 2):
	speed = float(sys.argv[2])
else:
	speed = 0

msg = ''
if (speed <= 0):
	speed = 0.2
	msg = " (default speed)"
elif (speed > MAX_SPEED):
	speed = MAX_SPEED
	msg = " (max speed)"


if (len(sys.argv) > 3):
	moveTime = float(sys.argv[3])
else:
	moveTime = 0.0
if (moveTime <= 0):
	moveTime = DEFAULT_MOVE_TIME

if (direction == "forward") or (direction == "backward"):
	print "  >> Move " + str(direction) + " at speed " + str(speed) + msg +" for " + str(moveTime) + " sec\n"
else:
	print "  >> Turn " + str(direction) + " at speed " + str(speed) + msg +" for " + str(moveTime) + " sec\n"

# define variables :
linearDirection = 0
rotationalDirection = 0

#init :
pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
twist = Twist()

# get command :
if (direction == "forward"):
		linearDirection = 1
elif (direction == "backward"):
		linearDirection = -1
elif (direction == "left"):
		rotationalDirection = 1
elif (direction == "right"):
		rotationalDirection = -1

# send command :

twist.linear.x = linearDirection * speed
twist.angular.z = rotationalDirection * speed
t1 = time.time()
t2 = t1
#print str(t1)
while(t2-t1 < moveTime):
	pub.publish(twist)
	t2 = time.time()
	#print str(t2-t1)

twist.linear.x = 0
twist.angular.z = 0
pub.publish(twist)

exit()
