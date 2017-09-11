from ximea import xiapi
import time

import numpy as np 
from threading import Thread


cam = xiapi.Camera()
print('Opening first camera...')
cam.open_device_by_SN("16770651")
print("First Camera Opened \n")

cam_2 = xiapi.Camera()
print('Opening second camera...')
cam_2.open_device_by_SN("16771351") # xiAPI: deleting camera context: dwID=16771351, ptr=0ed4c000 processID=00002B69

print("Second Camera Opened \n")

timeout = 5000

cam.set_exposure(10000)
cam_2.set_exposure(10000)

########## first camera
cam.set_imgdataformat('XI_RGB24')
cam.set_trigger_source('XI_TRG_SOFTWARE')
#print("cam.get_gpo_selector is: ", cam.get_gpo_selector())
#cam.set_gpo_selector("XI_GPO_PORT1")
#cam.set_gpo_mode("XI_GPO_EXPOSURE_ACTIVE")

########### second camera
cam_2.set_imgdataformat('XI_RGB24')
cam_2.set_trigger_source('XI_TRG_SOFTWARE')
#cam_2.set_trigger_source('XI_TRG_EDGE_RISING')
#print("cam_2.get_gpi_selector is:", cam_2.get_gpi_selector(),"\n")
#cam_2.set_gpi_selector("XI_GPI_PORT1")
#cam_2.set_gpi_mode("XI_GPI_TRIGGER")


#start data acquisition
print('Starting data acquisition...\n')
cam.start_acquisition()
cam_2.start_acquisition()



now = time.clock()
Thread(target = cam.set_trigger_software(1)).start()
Thread(target = cam_2.set_trigger_software(1)).start()
now_2 = time.clock()
print("time to set_trigger is：", now_2 - now)

print("waiting ...  \n")
#time.sleep(0.5)


#create instance of Image to store image data and metadata

now = time.clock()
img = xiapi.Image()
cam.get_image(img)
data_np = img.get_image_data_numpy()
print("time to get the data1 is：", now_2 - now)
print(data_np[1,1])

del data_np

now = time.clock()
img_2 = xiapi.Image()
cam_2.get_image(img_2, timeout)
data_np_2 = img_2.get_image_data_numpy()
print("time to get the data2 is：", now_2 - now)
print(data_np_2[1,1]) 

# those two command are needed to run CMOS mlti-time.
cam.stop_acquisition()
cam.close_device()

cam_2.stop_acquisition()
cam_2.close_device()
print('Two Cameras Closed !\n')