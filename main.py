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

class WirelessSensor:
    def __init__(self,_ip):
        self.ip = _ip
        self.scaleValue = 16 #This is the temperature scale value we believe will work
        communicate.connect(_ip)
    def sendMessage(self):
        response = communicate.send_message()
        return response


#communicate.connect(ip = '10.0.2.137')
#wts1 = WirelessSensor("10.0.2.137")
wts1 = WirelessSensor("10.0.2.142")
def pullData(wts):
    global i
    global xs
    global ys
    global tempMat
    #response = communicate.send_message()
    response = wts.sendMessage()
    #print(response)
    try:
        temps = [(float(t)/wts.scaleValue) for t in response]
        xs.append(i)
        ys.append(temps[0])
        if i==0:
            tempMat = np.array(temps)
        else:
            tempMat = np.vstack((tempMat,temps))
        #tempMat[i] = temps
    except TypeError:
        print("Connection must not be going through")
        pass
    i += 1
def recordData():
    global xs
    global ys

    time = str(datetime.datetime.now().strftime("%Y-%m-%dT%H.%M.%S")) #Removes ms element
    path ="Data/" + time + ".csv"
    with open(path,"w+") as f:
            writer = csv.writer(f, delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for n in xs:
                writer.writerow( ["Washington", "16:35", 26, 85, xs[n]] )

    
    f.close()
    if f.closed:
        print("Data saved as " + path)


if __name__== '__main__':
    try:
        while True:
            time.sleep(0.5)
            pullData(wts1)
    except KeyboardInterrupt:
        communicate.close_sock()
        pass
