#to construct a 2D map of the robot environment using only odometer and sonar sensors. In this experiment, the robot will be mapping the walls of 
#the room where it is able to detect the presence of obstacles using 8 sonar sensors. Every sensor will able to detect obstacle, read values and plot them. No prior knowledge of the environment is assumed, and the construction of map is depending on the robot autonomously. The use of sonar sensors with trigonometric and geometric approaches have made it possible to 
#identify most of the obstacles throughout its movement as normal localization and object detection are not completely error free in any robotic platform.

import urllib.request
import json
import time
import numpy as np
import math
import matplotlib.pyplot as plt
# Webserver address and port, use 127.0.0.1 instead of localhost, it will be resolved quicker
url = 'http://127.0.0.1:18080'
# estimate the position of angle using radius
radius = 0.6

# Run in an infinite loop
while True:

    # Use this to pause the script for 0.1 seconds,
    time.sleep(0.1)

    # Request data from the webserver and parse to a array
    res = urllib.request.urlopen(url).read()
    data = json.loads(res)
    #data from the server like sonar values and position
    position = data['relativePosition']
    position = data['absolutePosition']
    robot_x = position["x"]
    robot_y = position["y"]
    # Function accepts the degrees as input and converts it into its radians equivalent.
    robot_th = (position["th"])*(math.pi/180)
   
    sonar_0 = data['SonarData'][0]+radius
    sonar_1 = data['SonarData'][1]
    sonar_2 = data['SonarData'][2]
    sonar_3 = data['SonarData'][3]
    sonar_4 = data['SonarData'][4]
    sonar_5 = data['SonarData'][5]
    sonar_6 = data['SonarData'][6]
    sonar_7 = data['SonarData'][7]+radius
    
    # Sonar 0
    if sonar_0<3000:
        #rotation matrix
        rotationX = [math. cos(robot_th),(-math. sin(robot_th))]
        rotationY = [math. sin(robot_th),(math. cos(robot_th))]
        #coordinates with respect to robot centre
        s0=[[sonar_0*math.cos(math.pi/2)],[sonar_0*math.sin(math.pi/2)]]
        #rotation
        rx0=np.matmul(rotationX,s0)
        ry0=np.matmul(rotationY,s0)
        #translation
        tx0=rx0+robot_x
        ty0=ry0+robot_y
        plt.scatter(tx0,ty0)