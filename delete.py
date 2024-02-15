import numpy as np
import matplotlib.pyplot as plt
from math import sin, cos, radians

WIDTH, HEIGHT = 0, 0

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

def shape(height, points):
    angle = 360
    x = [0]
    y = [0]
    angle = np.linspace(0,2*3.14,points+1)
    

    separation = list(split(range(chunk_size), points))


    for i in range(0,points):    
        x = x + list(np.cos(angle[i])*np.linspace(0,1,len(separation[i]))+x[-1])
        y = y + list(np.sin(angle[i])*np.linspace(0,1,len(separation[i]))+y[-1])

    x = np.array(x)/np.max(y)*height
    y = np.array(y)/np.max(y)*height
        
    return [np.array(x)-(np.max(x)+np.min(x))/2+WIDTH/2,np.array(y)-(np.max(y)+np.min(y))/2+HEIGHT/2]




def rotate_point(point, angle, center_point=(0, 0)):
    """Rotates a point around center_point(origin by default)
    Angle is in degrees.
    Rotation is counter-clockwise
    """
    angle_rad = radians(angle % 360)
    # Shift the point so that center_point becomes the origin
    new_point = (point[0] - center_point[0], point[1] - center_point[1])
    new_point = (new_point[0] * cos(angle_rad) - new_point[1] * sin(angle_rad),
                 new_point[0] * sin(angle_rad) + new_point[1] * cos(angle_rad))
    # Reverse the shifting we have done
    new_point = (new_point[0] + center_point[0], new_point[1] + center_point[1])
    return new_point


def rotate_polygon(polygon, angle, center_point=(0, 0)):
    """Rotates the given polygon which consists of corners represented as (x,y)
    around center_point (origin by default)
    Rotation is counter-clockwise
    Angle is in degrees
    """
    rotated_polygon_x = []
    rotated_polygon_y = []
    for i in range(0,len(polygon[0])):
        rx,ry = rotate_point([polygon[0][i],polygon[1][i]], angle, center_point)
        rotated_polygon_x.append(rx)
        rotated_polygon_y.append(ry)
    print(rotated_polygon_x)
    
    return [rotated_polygon_x,rotated_polygon_y]


def rotation(data,plane,speed,direction = 'cw'):
    print(data[0])

    if plane == 'x-y':
        x,y=rotate_polygon(data, speed, center_point=(0, 0))
        
    if plane == 'x-z':
        print('fuck me')
        
    if plane == 'y-z':
        print('fuck me')

    return [x,y]
chunk_size = 10

signal = np.array(shape(300,5))


plane = 'x-y'
speed = 2
plotting = rotation(signal,plane,speed)

x = plotting[0]
y = plotting[1]

fig = plt.figure()
ax = fig.add_subplot()

plt.plot(signal[0],signal[1],'tab:orange',label='original')
plt.plot(x,y,'blue',label='rotated')

point = [100,100]

plt.plot(point[0],point[1],'red',label='point',marker ='o')

rpoint = rotate_point(point, 20, center_point=(0, 0))
plt.plot(rpoint[0],rpoint[1],'green',label='point',marker ='o')


plt.legend()
ax.set_aspect('equal', adjustable='box')
plt.show()