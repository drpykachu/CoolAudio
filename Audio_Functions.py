import pygame
import numpy as np
import sys
import wave
import os
from math import sin, cos, radians

chunk_size = 1024
pertubation = 35
rotation_speed = 0.5


WIDTH, HEIGHT = 800, 800
FPS = 60

def circle(radius):
    theta = np.linspace(0,2*3.14,chunk_size)
    x_circ = radius*np.cos(theta) + WIDTH/2
    y_circ = radius*np.sin(theta) + HEIGHT/2
    return [x_circ,y_circ]
    
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

    x = np.array(x)[:-1]/np.max(y)*height
    y = np.array(y)[:-1]/np.max(y)*height
        
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
    
    return [rotated_polygon_x,rotated_polygon_y]


def rotation(data,plane,speed,direction = 'cw', center_point=(0, 0)):

    if plane == 'x-y':
        x,y=rotate_polygon(data, speed, center_point=(WIDTH/2, HEIGHT/2))
        
    if plane == 'x-z':
        print('fuck me')
        
    if plane == 'y-z':
        print('fuck me')

    return [x,y]