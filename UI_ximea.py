from __future__ import unicode_literals
import sys
import os
import random
import time

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QInputDialog, QPushButton, QMainWindow, QApplication, QSpinBox, QLabel
from PyQt5.QtWidgets import QWidget, QAction, QTabWidget,QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import  QGroupBox, QDialog,QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

import numpy as np
from numpy import arange, sin, pi

import matplotlib
# Make sure that we are using QT5BB
matplotlib.use('Qt5Agg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import Ximea_cmos
from UI_figure_anim_imshow import UI_figure


progname = os.path.basename(sys.argv[0])
progversion = "0.1"

 
class App(QMainWindow):
 
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 tabs - pythonspot.com'
        self.left = 0
        self.top = 0
        self.width = 1000
        self.height = 800
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        self.table_widget = MyTableWidget(self)   # creat a Widgat.
        self.setCentralWidget(self.table_widget)  # set the Widget to be CentralWidget of QMainWindow.
 
        self.show()
 
class MyTableWidget(QWidget):        
 
    def __init__(self, parent):   
        super(QWidget, self).__init__(parent)

        self.amp = 1.0
        self.t=0
        self.cnt = 0

        self.layout = QVBoxLayout(self)           # create a Layout, which will be setted for self

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()   
        self.tab2 = QWidget()
        #self.tabs.resize(800,600) 
        
        self.tabs.addTab(self.tab1,"Tab 1")       # Add tabs
        self.tabs.addTab(self.tab2,"Tab 2")
 
        self.layout.addWidget(self.tabs)          # Add tabs to widget

        self.setLayout(self.layout)

        self.initalUI_tab_1()
        self.initalUI_tab_2()


    def initalUI_tab_1(self):
                                                         # Create first tab
        self.tab1_layout = QHBoxLayout(self)             # create a Layout, which will be setted for tab1

        self.tab1_layout_R = QVBoxLayout(self)


        self.button_scope_pre = QPushButton("Connecte to Scope")
        self.button_scope_pre.clicked.connect(self.connect_Scope)


        self.button_scope = QPushButton("Get Scope Figure")
        self.button_scope.clicked.connect(self.get_Scope_fig)

        self.button_plot_tab1 = QPushButton('Plot')           #button connected to `plot` method
        self.button_plot_tab1.clicked.connect(self.plot_tab1)

             # add buttons onto tabl1.layout
        self.tab1_layout_R.addWidget(self.button_scope_pre)
        self.tab1_layout_R.addWidget(self.button_scope)
        self.tab1_layout_R.addWidget(self.button_plot_tab1)

        self.tab1_layout.addStretch()                     # put the plot_layout right side
        self.tab1_layout.addLayout(self.tab1_layout_R)    # here is "addLayout" not "addWedget"
        self.tab1.setLayout(self.tab1_layout)             # set tab1.layout to be the layout of tabl1       

    def initalUI_tab_2(self):

        #################### Create Plot cavas widget ###################################################
                                                         # Create first tab
        self.tab2_layout = QHBoxLayout(self)             # create a Layout, which will be setted for tab_2
        
        self.tab2_layout_R = QVBoxLayout(self)

                
        print("matplotlib.is_interactive :", matplotlib.is_interactive())



        self.createGridLayout("Para setting panel")
        self.tab2_layout_R.addWidget(self.horizontalGroupBox)



        ##################           The left side of Table 2                    ###
        self.tab2_layout_L = QVBoxLayout(self)

        self.figure_L = plt.figure()        # a figure instance to plot on
                                               #if put "plt.ion" on the head, which will make two more figures idependently.
        #self.canvas_L = FigureCanvas(self.figure_L)
        #self.toolbar_L = NavigationToolbar(self.canvas_L, self) # this is the Navigation widget, it takes the Canvas widget and a parent
        

        self.button_plot_L = QPushButton('Make Plot')           # Just some button connected to `plot` method
        self.button_plot_L.clicked.connect(self.plot_L) 

        self.button_preparing_plot_L = QPushButton('Prepaering Plot')           # Just some button connected to `plot` method
        self.button_preparing_plot_L.clicked.connect(self.preparing_plot_L) 



        self.button_connect_L = QPushButton('Connect Ximea Camera')           # Just some button connected to `plot` method
        self.button_connect_L.clicked.connect(self.connect_Ximea_cmos)

        self.tab2_layout_L.addWidget(self.button_plot_L)
        self.tab2_layout_L.addWidget(self.button_preparing_plot_L)
        #self.tab2_layout_L.addWidget(self.toolbar_L)         # this also needed to show the Navigation of plot
        #self.tab2_layout_L.addWidget(self.canvas_L)          # add Canvas Widget(plot widget) onto tab_2
    
        self.tab2_layout_L.addWidget(self.button_connect_L)



        self.tab2_layout.addLayout(self.tab2_layout_L)
        self.tab2_layout.addStretch()                      # put the plot_layout right side
        self.tab2_layout.addLayout(self.tab2_layout_R)
        ############################################################################################

        self.tab2.setLayout(self.tab2_layout)              # set tab2.layout to be the layout of tab_2   


    


    def get_Scope_fig(self):
        pass

        

    def connect_Scope(self):
        pass

    def createGridLayout(self, layout_name):
        self.horizontalGroupBox = QGroupBox(layout_name)
        layout = QGridLayout()
        #layout.setColumnStretch(1, 4)
        #layout.setColumnStretch(2, 4)


        self.cmos_para_bt = QPushButton('Cmos para set', self)
        self.cmos_para_bt.clicked.connect(self.Cmose_para_set)

        self.expose_spinbox = QSpinBox()
        self.expose_spinbox.setRange(1,10000)
        self.expose_spinbox.setValue(8000)

        self.xpixs_spinbox = QSpinBox()
        self.xpixs_spinbox.setRange(1,2048)
        self.xpixs_spinbox.setValue(2048)

        self.xoffset_spinbox = QSpinBox()
        self.xoffset_spinbox.setRange(0,2048)
        self.xoffset_spinbox.setValue(0)

        self.ypixs_spinbox = QSpinBox()
        self.ypixs_spinbox.setRange(1,1088)
        self.ypixs_spinbox.setValue(1088)

        self.yoffset_spinbox = QSpinBox()
        self.yoffset_spinbox.setRange(0,1088)
        self.yoffset_spinbox.setValue(0)


 
        layout.addWidget(QLabel('Expose time'),0,0) 
        layout.addWidget(self.expose_spinbox,0,1) 

        layout.addWidget(QLabel('X pixs'),1,0) 
        layout.addWidget(self.xpixs_spinbox,1,1) 
        layout.addWidget(QLabel('X offset'),1,2) 
        layout.addWidget(self.xoffset_spinbox,1,3) 


        layout.addWidget(QLabel('Y pixs'),2,0) 
        layout.addWidget(self.ypixs_spinbox,2,1) 
        layout.addWidget(QLabel('Y offset'),2,2) 
        layout.addWidget(self.yoffset_spinbox,2,3) 

        layout.addWidget(QLabel('Cmos para set'),5,0) 
        layout.addWidget(self.cmos_para_bt,5,0)

 
        self.horizontalGroupBox.setLayout(layout)




#    def set_expose_time(self):
#            
#        self.ximea_cam.cam.set_exposure(self.expose_spinbox)
#        print("Expose time(us) is: ", self.expose_spinbox)

    
#    def set_y_offset(self):
#        self.y_offset, okPressed = QInputDialog.getInt(self, "Get integer","Percentage:", 0, 0, 1088, 1)
#        if okPressed:
#            print("Y offset is: ", self.y_offset)


    def single_data_gen(self, t=0):
        pass

    def NI_data_gen(self):

        pass

    def connect_Ximea_cmos(self):
        
        try:
            self.ximea_cam = Ximea_cmos.Ximea_app()
            print("The CMOS Camera connected ! ")
        except:     # if the cmos open, it will go to here
            if self.ximea_cam.cam.CAM_OPEN:
                print("The CMOS Camera already connected ! ")
            else:
                print("Fall to connect Cmos, Please do it agian ! ")

        #after the test, we need this line. Ortherwise, there is no plot at the first time you click "Preparing Plot" and "Make plot".
        #You need to click "Preparing Plot" and "Make plot" agine, then you could got the plot.
        #if you add "self.plot_L()", click "Preparing Plot" and "Make plot" one time, you could get the plot.
        self.plot_L()

    def Cmose_para_set(self):
        print("Cmos para setting")
        self.ximea_cam.cam.set_width(self.xpixs_spinbox.value())
        print("xpixs_spinbox.value is:", self.xpixs_spinbox.value())
        self.ximea_cam.cam.set_height(self.ypixs_spinbox.value())
        print("ypixs_spinbox.value is:", self.ypixs_spinbox.value())
        print("Cmos para set done !")


    def image_size(self):
        cnt = 1
        
        #print("imag_size is:", imag_size)
        while cnt:
            imag_size = [self.expose_spinbox.value(), 
                        self.xpixs_spinbox.value(), 
                        self.xoffset_spinbox.value(),  
                        self.xpixs_spinbox.value(), 
                        self.yoffset_spinbox.value() ]

            cam_data = self.ximea_cam.get_data(imag_size)
            yield cam_data

    def plot_L(self):


        try :                                                #check whether there is "self.figure_L", if it exists, then print its location  
            print("The figure_L is:", self.figure_L)
        except AttributeError:                               #if it does not exist, then we create it 
            print("\n")
            print("No figure_L")
            self.figure_L = plt.figure()        # a figure instance to plot on
            try :
                print("rebuilt the figure_L:", self.figure_L)  #if created, print the location
            except AttributeError:
                print("rebuilt fall")                          #if not created, raise the information

        self.size = self.image_size()
        self.cmos_app = UI_figure(self.figure_L, self.size)
        self.cmos_app.UI_Animation_plot()

    def preparing_plot_L(self):
        
        try:
            print("\n")
            print(" ---   Begin to delete the figure !  ")
            del self.cmos_app
            #self.cmos_app.close()
            print("Unsuccessfully delete self.cmos_app:", self.cmos_app)
        except AttributeError:
            print("Successfully delete self.cmos_app ! ")
           

        try:
            del self.figure_L #, self.canvas_L, self.toolbar_L
            print("Unsuccessfully delete self.figure_L:", self.figure_L)
        except AttributeError:
             print("Successfully delete self.figure_L ! ")

        
        print("It's ready to make a plot!")
        '''
        self.size = self.image_size()
        #size = []
        self.cmos_app = UI_figure(self.figure_L, self.size)
        print("self.cmos_app is :", self.cmos_app)
        self.cmos_app.UI_Animation_plot()
        '''



        """
        del self.data, self.cmos_app
        self.data = self.image_data()
        self.cmos_app = UI_figure(self.figure_L, self.data)
        self.cmos_app.UI_Animation_plot()
        """


    def array_data_gen(self, t = 0):
        cnt = 0
        sample_num = 300
        while cnt< 100*sample_num:
            t = (cnt*sample_num + np.linspace(0,sample_num-1,sample_num))*0.01
            data = np.sin(t)
            cnt +=1
            yield t, data

    def Rigol_data_gen(self):
        pass
    
    def plot_R(self):
        pass

 
    def plot_tab1(self):
        pass
        
        

 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    print("the last step!")
    sys.exit(app.exec_())