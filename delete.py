WIDTH, HEIGHT = 800, 800

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

def shape(widther, heighter, points):
    angle = 360
    x = [0]
    y = [0]
    angle = np.linspace(0,2*3.14,points+1)
    

    separation = list(split(range(chunk_size), points))


    for i in range(0,points):
        
        x = x + list(np.cos(angle[i])*np.linspace(0,widther,len(separation[i]))+x[-1])
        y = y + list(np.sin(angle[i])*np.linspace(0,heighter,len(separation[i]))+y[-1])
    
    return [np.array(x)-(np.max(x)+np.min(x))/2+WIDTH/2,np.array(y)-(np.max(y)+np.min(y))/2+HEIGHT/2]


import numpy as np
import matplotlib.pyplot as plt
chunk_size = 1024

signal = np.array(shape(300,300,5))


print(len(signal[0]))

fig = plt.figure()
ax = fig.add_subplot()
plt.plot(signal[0],signal[1],'-.')
ax.set_aspect('equal', adjustable='box')
plt.show()