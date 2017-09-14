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
       



class Camera_Panel(QWidget):
       
    def __init__(self, parent):   
        super(QWidget, self).__init__(parent)
  

        self.camera_layout = QVBoxLayout(self)   # create a camera Layout

        self.figure = plt.figure()        # a figure instance to plot on
                                               #if put "plt.ion" on the head, which will make two more figures idependently.

        self.button_plot = QPushButton('Make Plot')           # Just some button connected to `plot` method
        self.button_plot.clicked.connect(self.plot) 

        self.button_preparing_plot = QPushButton('Prepaering Plot')           # Just some button connected to `plot` method
        self.button_preparing_plot.clicked.connect(self.preparing_plot) 

        self.button_connect = QPushButton('Connect Ximea Camera')           # Just some button connected to `plot` method
        self.button_connect.clicked.connect(self.connect_Ximea_cmos)

        self.camera_layout.addWidget(self.button_plot)
        self.camera_layout.addWidget(self.button_preparing_plot)
        self.camera_layout.addWidget(self.button_connect)

        self.createGridLayout("Para setting panel")
        self.camera_layout.addWidget(self.horizontalGroupBox)




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
    

    def connect_Ximea_cmos(self):
        pass

    def Cmose_para_set(self):
        pass

    def preparing_plot(self):
        pass
    
    def plot(self):
        pass


