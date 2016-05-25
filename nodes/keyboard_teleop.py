#!/usr/bin/env python
####################################################### 
##             bendahmane.amine@gmail.com            ##
##            last update : Jan 31st, 2016           ##
#######################################################
##  Description: This program transforms the inputs  ## 
##      from the keyboard to velocity commands.      ##
#######################################################

# configuration :
MAX_SPEED = 0.4
MAX_ROTATIONAL_SPEED = 0.3

#######################################################
##      DO NOT CHANGE ANYTHING AFTER THIS LINE!      ##
#######################################################


import roslib
import rospy
import time
import tty, termios, sys
from geometry_msgs.msg import Twist
rospy.init_node('keyboard_teleop')
roslib.load_manifest('pioneer_teleop')

# define constants :
KEY_UP = 65
KEY_DOWN = 66
KEY_RIGHT = 67
KEY_LEFT = 68
KEY_Q = 81
KEY_Q2 = 113
KEY_S = 83
KEY_S2 = 115
MOVE_TIME = 0.01

# define variables :
speed = 0.0
rotationalSpeed = 0.0
keyPress = 0
linearDirection = 0
rotationalDirection = 0
linearSpeed = 0
rotationalSpeed = 0

# init :
pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
twist = Twist()

while(keyPress != KEY_Q) and (keyPress != KEY_Q2):

	print " - Wainting for key press \n"
	print "      > Arrows = move robot \n"
	print "      > s = stop \n"
	print "      > q = quit \n"

	# get char :
	keyPress = " "
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
 	keyPress = ord(ch)

	# test command :
	drive = 0
	if (keyPress == KEY_UP):
		linearDirection = 1
		print "  >> Inscrement linear speed\n"
	elif (keyPress == KEY_DOWN):
		linearDirection = -1
		print "  >> Decrement linear speed\n"
	elif (keyPress == KEY_LEFT):
		rotationalDirection = 1
		print "  >> Inscrement rotational speed\n"
	elif (keyPress == KEY_RIGHT):
		rotationalDirection = -1
		print "  >> Decrement rotational speed\n"
	elif (keyPress == KEY_S) or (keyPress == KEY_S2):
		linearSpeed = 0.0
		rotationalSpeed = 0.0
		linearDirection = 0.0
		rotationalDirection = 0.0
		print "  >> Stop robot\n"

	newLinearSpeed = linearSpeed + linearDirection * 0.1
	newRotationalSpeed = rotationalSpeed + rotationalDirection * 0.1

	if (newLinearSpeed > MAX_SPEED) or (newLinearSpeed < MAX_SPEED*(-1)):
		print "     Warning ! Maximum linar speed already reached\n"
	else:
		linearSpeed = newLinearSpeed

	if (newRotationalSpeed > MAX_SPEED) or (newRotationalSpeed < MAX_SPEED*(-1)):
		print "     Warning ! Maximum rotational speed already reached\n"
	else:
		rotationalSpeed = newRotationalSpeed

	print "     Speed = (linar: "+ str(linearSpeed) +", rotational: "+ str(rotationalSpeed) +")\n"
	
	# send command :
	twist = Twist()	
	twist.linear.x = linearSpeed
	twist.angular.z = rotationalSpeed
	t1 = time.time()
	t2 = t1
	while(t2-t1 < MOVE_TIME):
		pub.publish(twist)
		t2 = time.time()

	# reinit :
	linearDirection = 0
	rotationalDirection = 0

twist.linear.x = 0
twist.angular.z = 0
pub.publish(twist)
print "  >> Quit"
exit()
