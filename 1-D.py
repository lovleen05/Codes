import urllib.request
import matplotlib.animation as animation
import json
import time
import numpy as np
import math
import matplotlib
import matplotlib.pyplot as plt

# Webserver address and port, use 127.0.0.1 instead of localhost, it will be resolved quicker
url = 'http://127.0.0.1:18080'
# estimate the position of angle using radius
radius = 0.6

# initializing the points
points=np.random.rand(50,1)
points[:,0]*=5000
points.dump("pmatrix.dat")
#initializing the weights to the points
weights=np.ones((50,1))
weights.dump("wmatrix.dat")
fig=plt.figure()
image = matplotlib.image.imread('occupancyMaps/map1.png')

def func(i):

    # Use this to pause the script for 0.1 seconds,
    time.sleep(0.1)
    points=np.load("pmatrix.dat")
    image = matplotlib.image.imread('occupancyMaps/map1.png')
    weights=np.load("wmatrix.dat")
    url = "http://127.0.0.1:18080/"
    # Request data from the webserver and parse to a array
    res = urllib.request.urlopen(url).read()
    data = json.loads(res)
    #data from the server like sonar values and position
    robot_x = data['absolutePosition']['x']
    robot_y = data['absolutePosition']['y']
    son0=data['SonarData'][0]+radius
    # Function accepts the degrees as input and converts it into its radians equivalent.
    robot_th = (data['absolutePosition']['th'])*(math.pi/180)
    l=data['odometryData']['l']
    tr=data['odometryData']['tr']
    rw=data['odometryData']['rw']
    t1=data['odometryData']['t1']
    t2=data['odometryData']['t2']
    
    #update the weights of each particle
    #for each particle we simulate robot motion
    for i in range(50): # no pf points
        if points[i]>0 and points[i]<5000:
            #calculating sonar point
            set_x=son0*math.cos(robot_th+90*math.pi/180)+points[i]
            set_y=son0*math.sin(robot_th+90*math.pi/180)+robot_y
            #calculating occupancy grid index
            col=math.ceil(set_x/100)
            row=50-math.ceil(set_y/100)
            
            if row>=0 and row<=50 and col>=0 and col<=50:
                p=image[row][col][0]
                #comparing the actual value estimated sensor value 
                if son0<5000:
                    weights[i]=1-abs(p-0)
                else:
                    weights[i]=1-abs(p-1)
            else:
                weights[i]=np.random.rand(1,1)
        else:
            # if the point is outside than choose random value frm inside
            points[i]=5000*np.random.rand(1,1)
            set_x=son0*math.cos(robot_th+90*math.pi/180)+points[i]
            set_y=son0*math.sin(robot_th+90*math.pi/180)+robot_y
            col=math.ceil(set_x/100)
            row=50-math.ceil(set_y/100)
            if row>=0 and row<=50 and col>=0 and col<=50:
                p=image[row][col][0]
                if son0<5000:
                    weights[i]=1-abs(p-0)
                else:
                    weights[i]=1-abs(p-1)
            else:
                weights[i]=np.random.rand(1,1)
    weights-=min(weights)
    sumweights=np.sum(weights)
    # resample
    new_points=points
    for i in range(50):
        num_copies = np.random.uniform(1,1)*sumweights
        sw=0
        for j in range(len(weights)):
            sw=sw+weights[j]
            if sw>num_copies:
                new_points[i]=points[j]
                break
    points=new_points
    #odometry
    dx=(t1+t2)*math.pi*rw/tr*math.cos(robot_th)
    #shifting all the point into dx
    points+=dx
    #adding random vales to all the particles
    points=points+np.random.normal(0,10,(50,1))
    points.dump("pmatrix.dat")
    weights.dump("wmatrix.dat")
    plt.scatter(points[0],robot_y)
    
ani = animation.FuncAnimation(fig, func,interval=50)