import numpy as np



import matplotlib
# Make sure that we are using QT5BB
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

import matplotlib.animation as animation

import time

import Ximea_cmos


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
        Orthewise, you could not see the plot figure.

    4) "self.ax.figure.canvas.draw()", which redraw the figure, makes bad. should be delete.

    """  
    def __init__(self, figure, data_gen):
        ##  data_gen,  which is an generation function, not an array
        self.data_gen = data_gen
        #print(next(self.data_gen))

        ## get the "data_gen" image shape
        self.ini_data = np.array(next(self.data_gen))
        print("data_gen type is:", type(self.ini_data))
        self.sample_shape = (self.ini_data).shape
        print("self.sample_shape is:", self.sample_shape)

        self.pause = False


        self.figure = figure
        self.ax = figure.add_subplot(111)                       # a figure instance to plot on
        print("__init__ works !")
    
        # This line is very important, if you want it to be interactive mode when you use it as a module
        plt.ion()  

    def onClick(self,event):
        self.pause ^= True 
        print(self.pause)

    def UI_Animation_plot(self):
        ### note: not "self.im,"
        self.im = self.ax.imshow(self.ini_data, cmap=plt.get_cmap('jet'))
        #import to use "self.ax.plot" not "plt.plot" that will mix two figures
        #self.figure.canvas.mpl_connect('button_press_event', self.onClick)
        print("initial image done!")
        ani = animation.FuncAnimation(self.figure, self.updatefig, self.data_gen, interval=500,
                              repeat=True)
        # refresh canvas
        ########   "self.ax.figure.canvas.draw()" is used for module, which will be used in "UI_w_module.py"
        self.ax.figure.canvas.draw()  
        ########   "plt.show()" is used for selftest, 
        #plt.show()   

    def updatefig(self, data):
        self.im.set_array(data)
        print("return the data_gen to figure!")
        return self.im,

    def close(self):
        plt.cla()





if __name__=="__main__":

    fig = plt.figure()
    ax = fig.add_subplot(111)

    def f(x, y):
        return np.sin(x) + np.cos(y)

    x = np.linspace(0, 2 * np.pi, 120)
    y = np.linspace(0, 2 * np.pi, 100).reshape(-1, 1)

    def data_gen(cnt = 0):
        global x,y
        cnt = 0
        while cnt < 1000:
            cnt += 1
            x += np.pi / 15.
            y += np.pi / 20.
            yield f(x,y)
    
    # You cannot use "img_data()" directly in "UI_figure()". "img_data" is a "'function' object" not "data_gen()"
   #img_data = data_gen()

     
    ximea_cam = Ximea_cmos.Ximea_app()

    print("exposure time:",ximea_cam.cam.get_exposure())
    ximea_cam.cam.set_width(100)
    ximea_cam.cam.set_height(200)
    print("Size of image is:",ximea_cam.cam.get_width(),ximea_cam.cam.get_height())
    def image_data(cnt = 0):
        while cnt < 1000:
            cnt += 1
            yield ximea_cam.get_data()

    #  image_data got from ximea cmos


    img_data = image_data()
    
    app = UI_figure(fig, img_data)
    app.UI_Animation_plot()


