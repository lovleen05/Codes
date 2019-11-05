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
no_points=1000
# initializing the points
points=np.random.rand(no_points,2)
points[:,0]*=5000
points[:,1]*=5000
points.dump("pmatrix.dat")
#initializing the weights to the points
weights=np.ones((no_points,1))
weights.dump("wmatrix.dat")
fig=plt.figure()
image = matplotlib.image.imread('occupancyMaps/map1.png')

def func(i):

    # Use this to pause the script for 0.1 seconds,
    time.sleep(0.1)
    points=np.load("pmatrix.dat")
    no_points=len(points)
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
    for i in range(no_points): # no pf points
        if points[i][0]>0 and points[i][0]<5000 and points[i][1]>0 and points[i][1]<5000:
            #calculating sonar point
            set_x=son0*math.cos(robot_th+90*math.pi/180)+points[i][0]
            set_y=son0*math.sin(robot_th+90*math.pi/180)+points[i][1]
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
            if points[i][0]>5000 or points[i][0]<0:
                points[i][0]=5000*np.random.rand(1,1)
            if points[i][1]>5000 or points[i][1]<0:
                points[i][1]=5000*np.random.rand(1,1)
            set_x=son0*math.cos(robot_th+90*math.pi/180)+points[i][0]
            set_y=son0*math.sin(robot_th+90*math.pi/180)+points[i][1]
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
    for i in range(no_points):
        num_copies = np.random.uniform(1,1)*sumweights
        sw=0
        for j in range(len(weights)):
            sw=sw+weights[j]
            if sw>num_copies:
                new_points[i][0]=points[j][0]
                new_points[i][1]=points[j][1]
                break
    points=new_points
    #odometry
    dx=(t1+t2)*math.pi*rw/tr*math.cos(robot_th)
    dy=(t1+t2)*math.pi*rw/tr*math.sin(robot_th)
    #shifting all the points based on odometery
    for i in range(no_points):
        points[i][0]=points[i][0]+dx+np.random.normal(0,1)
        points[i][1]=points[i][1]+dy+np.random.normal(0,1)
    
    points.dump("pmatrix.dat")
    weights.dump("wmatrix.dat")
    listx=points[:,0]
    listy=points[:,1]
    plt.scatter(listx,listy)
    
ani = animation.FuncAnimation(fig, func,interval=50)
         
      
     
          
   
        
        
    
    
    
    
    
    
    
    
    