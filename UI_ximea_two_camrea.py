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

from Ximea_UI import Camera_Panel 
from UI_figure_anim_imshow import UI_figure

import Ximea_UI


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
        self.tab2 = QWidget()
        self.tabs.addTab(self.tab2,"Tab 2")
 
        self.layout.addWidget(self.tabs)          # Add tabs to widget
        self.setLayout(self.layout)

        camera_1_panel = Camera_Panel(self)

        self.tab2.setLayout(camera_1_panel.camera_layout)              # set tab2.layout to be the layout of tab_2   



 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    print("the last step!")
    sys.exit(app.exec_())