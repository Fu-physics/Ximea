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
        #self.button_scope_pre.clicked.connect(self.connect_Scope)


        self.button_scope = QPushButton("Get Scope Figure")
        #self.button_scope.clicked.connect(self.get_Scope_fig)

        self.button_plot_tab1 = QPushButton('Plot')           #button connected to `plot` method
        #self.button_plot_tab1.clicked.connect(self.plot_tab1)

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


            #########   camera 1 UI, which is on the left side of table 2
        self.camera_1 = QVBoxLayout(self)

        self.cmaera_1_up = QVBoxLayout(self)
        self.camera1_para("Camera 1 Para Setting Panel")
        self.cmaera_1_up.addWidget(self.camera1_GroupBox)

        self.cmaera_1_down = QHBoxLayout(self)
        self.figure_1 = plt.figure()        # a figure instance to plot on
                                               #if put "plt.ion" on the head, which will make two more figures idependently.
       
        self.button_plot_1 = QPushButton('Make Plot')           # Just some button connected to `plot` method
        self.button_plot_1.clicked.connect(self.plot_1) 

        self.button_preparing_plot_1 = QPushButton('Prepaering Plot')           # Just some button connected to `plot` method
        self.button_preparing_plot_1.clicked.connect(self.preparing_plot_1) 

        self.button_connect_1 = QPushButton('Connect Ximea Camera')           # Just some button connected to `plot` method
        self.button_connect_1.clicked.connect(self.connect_Ximea_cmos_1)

        self.cmaera_1_down.addWidget(self.button_connect_1)
        self.cmaera_1_down.addWidget(self.button_preparing_plot_1)
        self.cmaera_1_down.addWidget(self.button_plot_1)
        
        self.camera_1.addLayout(self.cmaera_1_up)
        #self.tab2_layout.addStretch()                      # put the plot_layout right side
        self.camera_1.addLayout(self.cmaera_1_down)


                #########   camera 2 UI, which is on the right side of table 2
        self.camera_2 = QVBoxLayout(self)

        self.cmaera_2_up = QVBoxLayout(self)
        self.camera2_para("Camera 2 Para Setting Panel")
        self.cmaera_2_up.addWidget(self.camera2_GroupBox)

        self.cmaera_2_down = QHBoxLayout(self)
        self.figure_2 = plt.figure()        # a figure instance to plot on
                                               #if put "plt.ion" on the head, which will make two more figures idependently.
       
        self.button_plot_2 = QPushButton('Make Plot')           # Just some button connected to `plot` method
        self.button_plot_2.clicked.connect(self.plot_2) 

        self.button_preparing_plot_2 = QPushButton('Prepaering Plot')           # Just some button connected to `plot` method
        self.button_preparing_plot_2.clicked.connect(self.preparing_plot_2) 

        self.button_connect_2 = QPushButton('Connect Ximea Camera')           # Just some button connected to `plot` method
        self.button_connect_2.clicked.connect(self.connect_Ximea_cmos_2)

        
        
        self.cmaera_2_down.addWidget(self.button_connect_2)
        self.cmaera_2_down.addWidget(self.button_preparing_plot_2)
        self.cmaera_2_down.addWidget(self.button_plot_2)


        self.camera_2.addLayout(self.cmaera_2_up)
        #self.tab2_layout.addStretch()                      # put the plot_layout right side
        self.camera_2.addLayout(self.cmaera_2_down)


        ####################################     put camera 1 on left and  2 on right                     ##########################

        self.tab2_layout.addLayout(self.camera_1)
        self.tab2_layout.addStretch()
        self.tab2_layout.addLayout(self.camera_2)

        self.tab2.setLayout(self.tab2_layout)              # set tab2.layout to be the layout of tab_2   
        

    def camera1_para(self, layout_name):
        self.camera1_GroupBox = QGroupBox(layout_name)
        layout = QGridLayout()
        #layout.setColumnStretch(1, 4)
        #layout.setColumnStretch(2, 4)


        self.cmos_para_bt_1 = QPushButton('Cmos para set', self)
        self.cmos_para_bt_1.clicked.connect(self.Cmose_para_set_1)

        self.expose_spinbox_1 = QSpinBox()
        self.expose_spinbox_1.setRange(1,10000)
        self.expose_spinbox_1.setValue(8000)

        self.xpixs_spinbox_1 = QSpinBox()
        self.xpixs_spinbox_1.setRange(1,2048)
        self.xpixs_spinbox_1.setValue(2048)

        self.xoffset_spinbox_1 = QSpinBox()
        self.xoffset_spinbox_1.setRange(0,2048)
        self.xoffset_spinbox_1.setValue(0)

        self.ypixs_spinbox_1 = QSpinBox()
        self.ypixs_spinbox_1.setRange(1,1088)
        self.ypixs_spinbox_1.setValue(1088)

        self.yoffset_spinbox_1 = QSpinBox()
        self.yoffset_spinbox_1.setRange(0,1088)
        self.yoffset_spinbox_1.setValue(0)

        layout.addWidget(QLabel('Expose time'),0,0) 
        layout.addWidget(self.expose_spinbox_1,0,1) 
        layout.addWidget(QLabel('X pixs'),1,0) 
        layout.addWidget(self.xpixs_spinbox_1,1,1) 
        layout.addWidget(QLabel('X offset'),1,2) 
        layout.addWidget(self.xoffset_spinbox_1,1,3) 
        layout.addWidget(QLabel('Y pixs'),2,0) 
        layout.addWidget(self.ypixs_spinbox_1,2,1) 
        layout.addWidget(QLabel('Y offset'),2,2) 
        layout.addWidget(self.yoffset_spinbox_1,2,3) 

        layout.addWidget(QLabel('Cmos para set'),5,0) 
        layout.addWidget(self.cmos_para_bt_1,5,0)

        self.camera1_GroupBox.setLayout(layout)



    def camera2_para(self, layout_name):
        self.camera2_GroupBox = QGroupBox(layout_name)
        layout = QGridLayout()
        #layout.setColumnStretch(1, 4)
        #layout.setColumnStretch(2, 4)


        self.cmos_para_bt_2 = QPushButton('Cmos para set', self)
        self.cmos_para_bt_2.clicked.connect(self.Cmose_para_set_2)

        self.expose_spinbox_2 = QSpinBox()
        self.expose_spinbox_2.setRange(1,10000)
        self.expose_spinbox_2.setValue(8000)

        self.xpixs_spinbox_2 = QSpinBox()
        self.xpixs_spinbox_2.setRange(1,2048)
        self.xpixs_spinbox_2.setValue(2048)

        self.xoffset_spinbox_2 = QSpinBox()
        self.xoffset_spinbox_2.setRange(0,2048)
        self.xoffset_spinbox_2.setValue(0)

        self.ypixs_spinbox_2 = QSpinBox()
        self.ypixs_spinbox_2.setRange(1,1088)
        self.ypixs_spinbox_2.setValue(1088)

        self.yoffset_spinbox_2 = QSpinBox()
        self.yoffset_spinbox_2.setRange(0,1088)
        self.yoffset_spinbox_2.setValue(0)

        layout.addWidget(QLabel('Expose time'),0,0) 
        layout.addWidget(self.expose_spinbox_2,0,1) 

        layout.addWidget(QLabel('X pixs'),1,0) 
        layout.addWidget(self.xpixs_spinbox_2,1,1) 
        layout.addWidget(QLabel('X offset'),1,2) 
        layout.addWidget(self.xoffset_spinbox_2,1,3) 
        layout.addWidget(QLabel('Y pixs'),2,0) 
        layout.addWidget(self.ypixs_spinbox_2,2,1) 
        layout.addWidget(QLabel('Y offset'),2,2) 
        layout.addWidget(self.yoffset_spinbox_2,2,3) 

        layout.addWidget(QLabel('Cmos para set'),5,0) 
        layout.addWidget(self.cmos_para_bt_2,5,0)

        self.camera2_GroupBox.setLayout(layout)


    def connect_Ximea_cmos_1(self):
        
        try:
            self.ximea_cam_1 = Ximea_cmos.Ximea_app(ID_str ='16770651')   ## plase use the ID, which is a string not integer number
            print("The CMOS Camera connected ! ")
        except:     # if the cmos open, it will go to here
            if self.ximea_cam_1.cam.CAM_OPEN:
                print("The CMOS Camera already connected ! ")
            else:
                print("Fall to connect Cmos, Please do it agian ! ")

        #after the test, we need this line. Ortherwise, there is no plot at the first time you click "Preparing Plot" and "Make plot".
        #You need to click "Preparing Plot" and "Make plot" agine, then you could got the plot.
        #if you add "self.plot_L()", click "Preparing Plot" and "Make plot" one time, you could get the plot.
        self.plot_1()

    def connect_Ximea_cmos_2(self):
        
        try:
            self.ximea_cam_2 = Ximea_cmos.Ximea_app(ID_str ='16770651')    ## plase use the ID, which is a string not integer number
            print("The CMOS Camera connected ! ")
        except:     # if the cmos open, it will go to here
            if self.ximea_cam_2.cam.CAM_OPEN:
                print("The CMOS Camera already connected ! ")
            else:
                print("Fall to connect Cmos, Please do it agian ! ")

        #after the test, we need this line. Ortherwise, there is no plot at the first time you click "Preparing Plot" and "Make plot".
        #You need to click "Preparing Plot" and "Make plot" agine, then you could got the plot.
        #if you add "self.plot_L()", click "Preparing Plot" and "Make plot" one time, you could get the plot.
        self.plot_2()

    def Cmose_para_set_1(self):
        print("Cmos_1 para setting")
        self.ximea_cam_1.cam.set_width(self.xpixs_spinbox_1.value())
        print("xpixs_spinbox_1.value is:", self.xpixs_spinbox_1.value())
        self.ximea_cam_1.cam.set_height(self.ypixs_spinbox_1.value())
        print("ypixs_spinbox_1.value is:", self.ypixs_spinbox_1.value())
        print("Cmos para set done !")

    def Cmose_para_set_2(self):
        print("Cmos_1 para setting")
        self.ximea_cam_2.cam.set_width(self.xpixs_spinbox_2.value())
        print("xpixs_spinbox_1.value is:", self.xpixs_spinbox_2.value())
        self.ximea_cam_2.cam.set_height(self.ypixs_spinbox_2.value())
        print("ypixs_spinbox_1.value is:", self.ypixs_spinbox_2.value())
        print("Cmos para set done !")


    def image_size_1(self):
        cnt = 1
        
        #print("imag_size is:", imag_size)
        while cnt:
            imag_size = [self.expose_spinbox_1.value(), 
                        self.xpixs_spinbox_1.value(), 
                        self.xoffset_spinbox_1.value(),  
                        self.xpixs_spinbox_1.value(), 
                        self.yoffset_spinbox_1.value() ]

            cam_data = self.ximea_cam_1.get_data(imag_size)
            yield cam_data

    def image_size_2(self):
        cnt = 1
        
        #print("imag_size is:", imag_size)
        while cnt:
            imag_size = [self.expose_spinbox_2.value(), 
                        self.xpixs_spinbox_2.value(), 
                        self.xoffset_spinbox_2.value(),  
                        self.xpixs_spinbox_2.value(), 
                        self.yoffset_spinbox_2.value() ]

            cam_data = self.ximea_cam_2.get_data(imag_size)
            yield cam_data

    def plot_1(self):


        try :                                                #check whether there is "self.figure_1", if it exists, then print its location  
            print("The figure_1 is:", self.figure_1)
        except AttributeError:                               #if it does not exist, then we create it 
            print("\n")
            print("No figure_1")
            self.figure_1 = plt.figure()        # a figure instance to plot on
            try :
                print("rebuilt the figure_1:", self.figure_1)  #if created, print the location
            except AttributeError:
                print("rebuilt fall")                          #if not created, raise the information

        cam_data_1 = self.image_size_1()
        self.cmos_app_1 = UI_figure(self.figure_1, cam_data_1)
        self.cmos_app_1.UI_Animation_plot()

    def plot_2(self):


        try :                                                #check whether there is "self.figure_1", if it exists, then print its location  
            print("The figure_2 is:", self.figure_2)
        except AttributeError:                               #if it does not exist, then we create it 
            print("\n")
            print("No figure_2")
            self.figure_2 = plt.figure()        # a figure instance to plot on
            try :
                print("rebuilt the figure_2:", self.figure_2)  #if created, print the location
            except AttributeError:
                print("rebuilt fall")                          #if not created, raise the information

        cam_data_2 = self.image_size_2()
        self.cmos_app_2 = UI_figure(self.figure_2, cam_data_2)
        self.cmos_app_2.UI_Animation_plot()

    def preparing_plot_1(self):
        
        try:
            print("\n")
            print(" ---   Begin to delete the figure !  ")
            del self.cmos_app_1
            #self.cmos_app.close()
            print("Unsuccessfully delete self.cmos_app_1:", self.cmos_app_1)
        except AttributeError:
            print("Successfully delete self.cmos_app_1 ! ")
           

        try:
            del self.figure_1 #, self.canvas_L, self.toolbar_L
            print("Unsuccessfully delete self.figure_1:", self.figure_1)
        except AttributeError:
             print("Successfully delete self.figure_1 ! ")
        print("It's ready to make a plot!")


    def preparing_plot_2(self):
        
        try:
            print("\n")
            print(" ---   Begin to delete the figure !  ")
            del self.cmos_app_2
            #self.cmos_app.close()
            print("Unsuccessfully delete self.cmos_app_2:", self.cmos_app_2)
        except AttributeError:
            print("Successfully delete self.cmos_app_2 ! ")
           

        try:
            del self.figure_2 #, self.canvas_L, self.toolbar_L
            print("Unsuccessfully delete self.figure_2:", self.figure_2)
        except AttributeError:
             print("Successfully delete self.figure_2 ! ")
        print("It's ready to make a plot!")


    def array_data_gen(self, t = 0):
        cnt = 0
        sample_num = 300
        while cnt< 100*sample_num:
            t = (cnt*sample_num + np.linspace(0,sample_num-1,sample_num))*0.01
            data = np.sin(t)
            cnt +=1
            yield t, data

 
        

 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    print("the last step!")
    sys.exit(app.exec_())