#!/usr/bin/env python
####################################################### 
##             bendahmane.amine@gmail.com            ##
##            last update : Jan 31st, 2016           ##
#######################################################
##  Description: This program transforms the inputs  ## 
##  from the keyboard to discrete velocity commands  ##
##  (by default, the robot moves for 1 second only)  ##
#######################################################

# configuration :
MAX_SPEED = 0.3
MAX_ROTATIONAL_SPEED = 0.3
MOVE_TIME = 1

#######################################################
##      DO NOT CHANGE ANYTHING AFTER THIS LINE!      ##
#######################################################

import roslib
import rospy
import time
import tty, termios, sys
from geometry_msgs.msg import Twist
rospy.init_node('discrete_keyboard_teleop')
roslib.load_manifest('pioneer_teleop')

# define constants :
KEY_UP = 65
KEY_DOWN = 66
KEY_RIGHT = 67
KEY_LEFT = 68
KEY_PLUS = 43
KEY_MINUS = 45
KEY_Q = 81
KEY_Q2 = 113

# define variables :
speed = 0.1
rotationalSpeed = 0.0
keyPress = 0
linearDirection = 0
rotationalDirection = 0

#init :
pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
twist = Twist()

while(keyPress != KEY_Q) and (keyPress != KEY_Q2):

	print " - Wainting for key press \n"
	print "      > Arrows = move robot \n"
	print "      > +/- = change speed \n"
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
		drive = 1
		print "  >> Move forward at speed " + str(speed) + " for " + str(MOVE_TIME) + " sec\n"
	elif (keyPress == KEY_DOWN):
		linearDirection = -1
		drive = 1
		print "  >> Move backward at speed " + str(speed) + " for " + str(MOVE_TIME) + " sec\n"
	elif (keyPress == KEY_LEFT):
		rotationalDirection = 1
		drive = 1
		print "  >> Turn left at speed " + str(speed) + " for " + str(MOVE_TIME) + " sec\n"
	elif (keyPress == KEY_RIGHT):
		rotationalDirection = -1
		drive = 1
		print "  >> Turn Right at speed " + str(speed) + " for " + str(MOVE_TIME) + " sec\n"
	elif (keyPress == KEY_PLUS) and (speed < MAX_SPEED):
		speed += 0.1
		print "  >> Set speed to " + str(speed) + "\n"
	elif (keyPress == KEY_PLUS):
		print "  >> Maximum speed value already reached : " + str(MAX_SPEED)	
	elif (keyPress == KEY_MINUS) and (speed > 0.1):
		speed -= 0.1
		print "  >> Set speed to " + str(speed) + "\n"
	elif (keyPress == KEY_MINUS):
		print "  >> Minimum speed value already reached : 0.1"

	if (drive):
		if (speed > MAX_ROTATIONAL_SPEED):
			rotationalSpeed = MAX_ROTATIONAL_SPEED
		else:
			rotationalSpeed = speed

		# send command :
		twist.linear.x = linearDirection * speed
		twist.angular.z = rotationalDirection * rotationalSpeed
		pub.publish(twist)
		t1 = time.time()
		t2 = t1
		while(t2-t1 < MOVE_TIME):
			pub.publish(twist)
			t2 = time.time()

		twist.linear.x = 0
		twist.angular.z = 0
		pub.publish(twist)

		# reinit :
		rotationalSpeed = 0.0
		linearDirection = 0
		rotationalDirection = 0

print "  >> Quit"
exit()
