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
resol=100
cols = 200
rows = 200
grid = [[0 for i in range(cols)] for j in range(rows)]
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
    
    i= math.ceil(cols/2-robot_y/resol)
    j= math.ceil(rows/2+robot_x/resol)
    grid[i][j]=2
    
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
        #plt.scatter(tx0,ty0)
        i= math.ceil(cols/2-ty0/resol)
        j= math.ceil(rows/2+tx0/resol)
        grid[i][j]=1
    plt.imshow(grid)
