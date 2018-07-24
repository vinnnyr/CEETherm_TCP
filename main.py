#!/usr/bin/env python
import time
import communicate
import numpy as np
#import graph

global xs
global ys
global tempMat

global i

xs = []
ys = []
tempMat = []
i = 0

communicate.connect(ip = '10.0.2.137')
scaleValue = 16 #This is the temperature scale value we believe will work

def pullData():
    global i
    global xs
    global ys
    global tempMat
    response = communicate.send_message()
    try:
        temps = [(float(t)/scaleValue) for t in response]
        xs.append(i)
        ys.append(temps[0])
        if i==0:
            tempMat = np.array(temps)
        else:
            tempMat = np.vstack((tempMat,temps))
        #tempMat[i] = temps
    except TypeError:
        #communicate.try_reset()
        print("Error, or no temperature reported")
    i += 1

if __name__== '__main__':
    try:
        while True:
            time.sleep(0.5)
            pullData()
    except KeyboardInterrupt:
        communicate.close_sock()
        pass
