#!/usr/bin/env python
import time
import communicate
#import graph

global xs
global ys
global i

xs = []
ys = []
i = 0

communicate.connect(ip = '10.0.2.137')
scaleValue = 16 #This is the temperature scale value we believe will work

def pullData():
    global i
    response = communicate.send_message()
    try:
        temps = [(float(t)/scaleValue) for t in response]
        #print(temps)
        xs.append(i)
        ys.append(temps[0])
    except:
        #communicate.try_reset()
        print("No temperature reported")
    i += 1

if __name__== '__main__':
    try:
        while True:
            time.sleep(0.5)
            pullData()
    except KeyboardInterrupt:
        communicate.close_sock()
        pass
