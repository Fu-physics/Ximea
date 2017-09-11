import threading
from threading import Thread
import time 


def func1():
    
    print ('Working func111111111111')
    time.sleep(1)
    print (time.time())

def func2():

    print ('Working func22222222222')
    time.sleep(1)
    print (time.time())


if __name__ == '__main__':

    Thread(target = func1).start()

    Thread(target = func2).start()