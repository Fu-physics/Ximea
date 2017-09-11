import numpy as np
from numpy import arange, sin, pi

import matplotlib
# Make sure that we are using QT5BB
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

import matplotlib.animation as animation

import nidaqmx
import time


class UI_figure:  
    """
    1) This module is for creating a figure plot using data of "data_gen".
            (1) "data_gen" is a generator function, iterable or int, cannot be a simple data. 
            (2) "figure" is a object, "plt.figure()"
            (3) "method" is a string, must be "add" or "renew"
                  "add"   : add the new datas into plot
                  "renew" : abort previous figure frame, just plot the newdatas. 

    2) data = self.data_gen, which is passed from outside. 
            the  self.data_gen must be generated like this way:

                " def data_gen():
                     ....
                     yield t, amp
                "
                it is a two dimensional np.array datas generated from generator function. 
                If you want see the datas, there are two ways:
                    1) next(data_gen())
                    2) for t, amp in data_gen():
                            print(t, amp)


    3) If you want use this module independently, such as selftest, you need to make some change.
            (1) delete "plt.ion()"
            (2) change "self.ax.figure.canvas.draw()" to be "plt.show()"
        Orthewise, you could not see the plot figure and get the error.

    4) "self.ax.figure.canvas.draw()", which redraw the figure, makes bad. should be delete.

    """  
    def __init__(self, figure, data_gen, method = "add", plot_axis = [0,0,0,0]):
        ##  data_gen,  which is an iterable data, not an array
        self.plot_axis = plot_axis
        self.data_gen = data_gen
        #print(next(self.data_gen))
        sample_1 = np.array(next(self.data_gen)[1])
        print("sample_1 type is:", type(sample_1))
        self.sample_num = int(sample_1.size)
        print("self.sample_num is:", self.sample_num)

        self.method = method

        self.figure = figure
        self.ax = figure.add_subplot(111)                       # a figure instance to plot on
        #print("__init__ works !")
    
        # This line is very important, if you want it to be interactive mode when you use it as a module
        plt.ion()   


    def UI_Animation_plot(self):
        self.line, = self.ax.plot([], [], animated=True)  
        #import to use "self.ax.plot" not "plt.plot" that will mix two figures
        self.xdata = np.array([])
        self.ydata = np.array([])
        self.line.set_data(self.xdata, self.ydata) 
        self.ax.set_ylim(-2, 2)
        self.ax.set_xlim(0, 50)
        if self.plot_axis == [0,0,0,0]:
            pass
        else:
            self.xmin, self.xmax, self.ymin, self.ymax = self.plot_axis
            self.ax.set_xlim(self.xmin, self.xmax)
            self.ax.set_ylim(self.ymin, self.ymax)

        ani = animation.FuncAnimation(self.figure, self.plot_method, self.data_gen, blit=True, interval=10,
                              repeat=True)
        # refresh canvas
        ########   "self.ax.figure.canvas.draw()" is used for module, which will be used in "UI_w_module.py"
        self.ax.figure.canvas.draw()  
        ########   "plt.show()" is used for selftest, 
        #plt.show()   

    def plot_method(self, data):

        x, y = data
        #
        #print("x is:" , x)
        #print("y is:" , y)
        xmin, xmax = self.ax.get_xlim()
        if self.method == "add":
            self.xdata = np.append(self.xdata, x)
            self.ydata = np.append(self.ydata, y)
            #print("xdata is:", self.xdata, ";    ", "ydata is:", self.ydata)

            if self.sample_num == 1:
                #print("sample_num (single data add) is:", self.sample_num)
                if x >= xmax:
                    self.ax.set_xlim(xmax, 2*xmax)
                    # self.ax.figure.canvas.draw()
                    # #normally, there is no need to redraw the plot, as we will return the "line,"
                    print("figure_axes changed")

            elif self.sample_num > 1:
                #print("sample_num (array data add) is:", self.sample_num)
                    #print("sample_num (single data add) is:", self.sample_num)
                if x[self.sample_num - 1] >= xmax:
                    self.ax.set_xlim(xmax, 2 * xmax )
                    #self.ax.figure.canvas.draw() 
                    # #normally, there is no need to redraw the plot, as we will return the "line,"
                    print("figure_axes changed")


        elif self.method == "renew":
            #print("sample_num (array data renew) is:", self.sample_num)
            self.xdata = x
            self.ydata = y
            #print("self.xdata is:", self.xdata)
            #x_min = np.amin(self.xdata)
            #x_max = np.amax(self.xdata)
            #y_min = np.amin(self.ydata)
            #y_max = np.amax(self.ydata)
            #self.ax.set_xlim(x_min - abs(x_min)/2, x_max- abs(x_max)/2)
            #self.ax.set_ylim(y_min - abs(y_min)/2, y_max- abs(y_max)/2)
            #print("x_min", x_min, "y_min", y_min)
            #print("x_max", x_max, "y_max", y_max)

        else:
            print("Method Error!")  
        #print(self.xdata)
        self.line.set_data(self.xdata, self.ydata)
        #print("self.line, is:", self.line,)
        return self.line,


if __name__=="__main__":
    print(__name__)
    figure = plt.figure()

    def single_data_gen(t=0):
        cnt = 0
        t = 0
        while cnt < 1000:
            cnt += 1
            t += 0.1
            yield t, np.sin(t)

    def array_data_gen(t = 0):
        cnt = 0
        sample_num = 300
        while cnt< 100*sample_num:
            t = (cnt*sample_num + np.linspace(0,sample_num-1,sample_num))*0.01
            data = np.sin(t)
            cnt +=1
            yield t, data

    method = "add"
    #method = "renew"
    plot_axis =[0,50,-1,1]

    #data = single_data_gen()
    data = array_data_gen()

    print("------",  method, "---" , data, "------")
    
    app = UI_figure(figure, data, method, plot_axis)
    app.UI_Animation_plot()

