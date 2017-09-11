from ximea import xiapi

#create instance for cameras
cam1 = xiapi.Camera(dev_id=0)
cam2 = xiapi.Camera(dev_id=1)

#start communication
print('Opening cameras...')
cam1.open_device()
cam2.open_device()

#print device serial numbers
print('Camera 1 serial number: ' + str(cam1.get_device_sn()))
print('Camera 2 serial number: ' + str(cam2.get_device_sn()))

#stop communication
cam1.close_device()
cam2.close_device()

print('Done.')



