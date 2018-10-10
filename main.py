#!/usr/bin/env python
import time
import datetime
import communicate
import numpy as np
import os
import csv

#import graph
global xs
global ys
global tempMat

global i

xs = []
ys = []
tempMat = []
i = 0

class WirelessSensor: #This is a class we use to define the temperature sensor values
    def __init__(self,_ip):
        self.ip = _ip
        self.scaleValue = 16 #This is the temperature scale value we believe will work
        communicate.connect(_ip)
    def sendMessage(self):
        response = communicate.send_message()
        return response

def pullData(wts):
    global i
    global xs
    global ys
    global tempMat
    #response = communicate.send_message()
    response = wts.sendMessage()
    #print(response)
    try:
        temps = [(float(t)/wts.scaleValue) for t in response] #Temperature in deg C
        print(temps)
        xs.append(i) #Vector of indexes
        ys.append(temps[0]) #Vector of temperatures
        if i==0: #If this is the first, create the array
            tempMat = np.array(temps)
        else:#If not, stack the values vertically so we have history
            tempMat = np.vstack((tempMat,temps))
        #tempMat[i] = temps
    except TypeError:
        print("Connection must not be going through")
        pass
    i += 1

wts1 = WirelessSensor("10.0.2.151") #The IP of the module we are interested in (Exhaust Air Temperature)

if __name__== '__main__':
    try:
        while True: #Main loop
            time.sleep(0.5) #Delay
            pullData(wts1) #pull data, store in global variables
    except KeyboardInterrupt: # ctrl + c
        communicate.close_sock()
        pass
