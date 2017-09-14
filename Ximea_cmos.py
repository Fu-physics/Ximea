import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from ximea import xiapi

import time

class Ximea_app():
    def __init__(self, ID_str ='16770651'):
        #create instance for first connected camera
        #start communication
        #to open specific device, use:
        self.cam = xiapi.Camera()
        print('Opening first camera...')
        #self.cam.open_device()
        self.cam.open_device_by_SN(ID_str)
        print("Camera Opened \n")
        self.cam.set_exposure(10000)

        self.cam.set_imgdataformat('XI_RGB24')
        #create instance of Image to store image data and metadata
        self.img = xiapi.Image()

        #start data acquisition
        print('Starting data acquisition...')
        self.cam.start_acquisition()


    def get_data(self, imag_size = [0,0,0,0]):
        ''''
        if not imag_size:
            print("image size not set")
        else:
            #self.cam.set_exposure(imag_size[0])
            #self.ximea_cam.cam.set_width(self.expose_spinbox.value())
            self.cam.set_width(imag_size[1])
            self.cam.set_offsetX(imag_size[2])
            self.cam.set_height(imag_size[3])
            self.cam.set_offsetY(imag_size[4])
        '''
        #print("imag_size", imag_size)
        #get data and pass them from camera to img
        now = time.clock()
        self.cam.get_image(self.img)
        #get raw data from camera
        #for Python2.x function returns string
        #for Python3.x function returns bytes
        data_np = self.img.get_image_data_numpy(invert_rgb_order=True)
        
        print ("\n\nIt took " + str(time.clock() - now) + "to get the image data")
        #print(data_np)
        #print("image data shape is:", data_np.shape)
        return data_np


if __name__ == "__main__":
    
    ximea_cam = Ximea_app()
    ## "imgdata_np" is a generation function
    

    fig = plt.figure()
    ax = fig.add_subplot(111)

    def image_data():
        yield ximea_cam.get_data()

    print(ximea_cam.cam.get_width(),ximea_cam.cam.get_height())
    ini_data = np.zeros((1088,2048))
    im = ax.imshow(ini_data, cmap=plt.get_cmap('jet'))

    i  = 1
    def updatefig(data):
        global i
        i = i + 1
        im.set_array(data)
        print( i ,"th time plot")
        return im,

    ani = animation.FuncAnimation(fig, updatefig, image_data, interval=500, blit=True)
    plt.show()

    print("-----  The end !  --------")

