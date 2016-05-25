#!/usr/bin/env python
####################################################### 
##             bendahmane.amine@gmail.com            ##
##            last update : Jan 31st, 2016           ##
#######################################################
##  Description: This program transforms the inputs  ## 
##      recieved from socket and the calls the       ##
##	         commandline_teleop.py program.          ##
#######################################################

MAX_SPEED = 0.4
DEFAULT_MOVE_TIME = 1.5
DEFAULT_PORT = 50001

FORWARD_ALIAS = 'forward' 
BACKWARD_ALIAS = 'backward'
LEFT_ALIAS = 'left'
RIGHT_ALIAS = 'right'

#######################################################
##      DO NOT CHANGE ANYTHING AFTER THIS LINE!      ##
#######################################################

import roslib
import rospy 
import socket
import sys
import os
rospy.init_node('teleop')
roslib.load_manifest('pioneer_teleop')

if (len(sys.argv) > 1):
	port = int(sys.argv[1])
	if (port <= 0):
		port = DEFAULT_PORT
else:
	port = DEFAULT_PORT

if (len(sys.argv) > 2):
	speed = float(sys.argv[2])
else:
	speed = 0
if (speed <= 0):
	speed = 0.2
elif (speed > MAX_SPEED):
	speed = MAX_SPEED

if (len(sys.argv) > 3):
	moveTime = float(sys.argv[3])
else:
	moveTime = 0.0
if (moveTime <= 0):
	moveTime = DEFAULT_MOVE_TIME

host = '' 
queue = 5
bufferSize = 256
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
serverSocket.bind(('',port)) 
serverSocket.listen(queue)

print " - Listening for network communications in port " + str(port) + "...\n"

while 1: 
	print " - Waiting for client...\n"
	clientSocket, address = serverSocket.accept()
	command = clientSocket.recv(bufferSize)
	if (command == 'forward') or (command == FORWARD_ALIAS):
		print "  >> Command recieved: move forward\n"
		os.system("rosrun pioneer_teleop commandline_teleop.py forward " + str(speed) + " " + str(moveTime))
	elif (command == 'backward') or (command == BACKWARD_ALIAS):
		print "  >> Command recieved: move backward\n"
		os.system("rosrun pioneer_teleop commandline_teleop.py backward " + str(speed) + " " + str(moveTime))
	elif (command == 'right') or (command == RIGHT_ALIAS):
		print "  >> Command recieved: move right\n"
		os.system("rosrun pioneer_teleop commandline_teleop.py right " + str(speed) + " " + str(moveTime))
	elif (command == 'left') or (command == LEFT_ALIAS):
		print "  >> Command recieved: move left\n"
		os.system("rosrun pioneer_teleop commandline_teleop.py left " + str(speed) + " " + str(moveTime))
	else:
		print "  >> Error: Command '" + command + "' not recognized !\n"
		print "            Please use " + str(FORWARD_ALIAS) + "," + str(BACKWARD_ALIAS) + "," + str(LEFT_ALIAS) + " or " + str(RIGHT_ALIAS) + "."
    	clientSocket.close()
