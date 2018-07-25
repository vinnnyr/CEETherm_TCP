#!/usr/bin/env python
import Tkinter as tk

import main

# The usage of matplotlib TkAgg makes this only work on Windows. There is a chance of this working on all platforms if in Python 3
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

import numpy as np

style.use('ggplot')
LARGE_FONT= ("Verdana", 12)

#Defining figure to look at:
f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)

def dataStream():
    main.pullData(main.wts1)
    t = main.xs
    y = main.ys
    yMat = main.tempMat
    return t,y,yMat

def animate(i):
    t,y,yMat = dataStream()
    a.clear()
    #print(yMat)

    l1, = a.plot(t,yMat.T[0],label="TC1")
    l2, = a.plot(t,yMat.T[1],label="TC2")
    l3, = a.plot(t,yMat.T[2],label="TC3")
    l4, = a.plot(t,yMat.T[3],label="TC4")
 
    #a.legend(handles=[l1,l2,l3,l4] )
    #a.legend( )
    a.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        root = tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {} #All frames are stored here
        for F in (StartPage,GraphPage):
            frame = F(container,self)
            self.frames[F] = frame
            frame.grid(row=0,column=0,sticky="nsew")
        self.show_frame(StartPage) #Start with the start page

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
     
     def __init__(self,parent,controller):
        
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = tk.Button(self, text="Graph Page",command=lambda: controller.show_frame(GraphPage)) #Button for first graph page
        button.pack()

class GraphPage(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self,text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = tk.Button(self,text="Back to Home", command = lambda : controller.show_frame(StartPage))
        button.pack()

        canvas = FigureCanvasTkAgg(f,self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand = True)

        toolbar = NavigationToolbar2TkAgg(canvas,self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand = True)

if __name__ == '__main__':
    mainApp = App()
    ani = animation.FuncAnimation(f, animate, interval=1000)
    mainApp.mainloop()
    main.communicate.close_sock() #Close the socket as soon as we are done (we close the window)