from ximea import xiapi
import time

import numpy as np 
from threading import Thread



cam_1 = xiapi.Camera()
print("Number of cameras is:", cam_1.get_number_devices(), "\n")
cam_1.open_device_by_SN("16770651")
print("First Camera Opened \n")

cam_2 = xiapi.Camera()
cam_2.open_device_by_SN("16771351") # xiAPI: deleting camera context: dwID=16771351, ptr=0ed4c000 processID=00002B69
print("Second Camera Opened \n")

timeout = 5000

#cam_1.set_exposure(10000)
#cam_2.set_exposure(10000)

########## first camera set trigger mode on camera1 - as master
cam_1.set_imgdataformat('XI_RGB24')
cam_1.set_trigger_source('XI_TRG_SOFTWARE')
#print("cam.get_gpo_selector is: ", cam_1.get_gpo_selector())
cam_1.set_gpo_selector("XI_GPO_PORT1")
cam_1.set_gpo_mode("XI_GPO_EXPOSURE_ACTIVE")

########### second camera set trigger mode on camera2 - as slave
cam_2.set_imgdataformat('XI_RGB24')
#cam_2.set_trigger_source('XI_TRG_SOFTWARE')
cam_2.set_trigger_source('XI_TRG_EDGE_RISING')
#print("cam_2.get_gpi_selector is:", cam_2.get_gpi_selector(),"\n")
cam_2.set_gpi_selector("XI_GPI_PORT1")
cam_2.set_gpi_mode("XI_GPI_TRIGGER")



#start data acquisition
print('Starting data acquisition...\n')
cam_1.start_acquisition()
cam_2.start_acquisition()

print("waiting ...  \n")
time.sleep(0.5)

# trigger acquisition on Master camera
cam_1.set_trigger_software(1)


#create instance of Image to store image data and metadata
now = time.clock()
img_1 = xiapi.Image()
cam_1.get_image(img_1)
data_np = img_1.get_image_data_numpy()
print("time to get the data1 is：", time.clock() - now)
print(data_np[1,1])

del data_np

now = time.clock()
img_2 = xiapi.Image()
cam_2.get_image(img_2, timeout)
data_np_2 = img_2.get_image_data_numpy()
print("time to get the data2 is：", time.clock() - now)
print(data_np_2[1,1]) 

# those two command are needed to run CMOS mlti-time.
cam_1.stop_acquisition()
cam_1.close_device()

cam_2.stop_acquisition()
cam_2.close_device()
print('Two Cameras Closed !\n')