#!/usr/bin/python3

import datetime
import threading
import logging
import random
import time

from cmd_basic_set import *
from cmd_supervision import *


BASIC_SET_TASK_DELAY_MIN = 4
BASIC_SET_TASK_DELAY_MAX = 5

SUPERVISION_TASK_DELAY_MIN = 4
SUPERVISION_TASK_DELAY_MAX = 5

#
# Basic Set Task
#
def ztask_basic_set(mutex):

    logging.info('get_basic_set started')
    
    sequence = 0
    while(True):
        
        sequence += 1
        if(sequence > 15):
            sequence = 0
            
        try:
            mutex.acquire(timeout=BASIC_SET_TASK_DELAY_MAX)
            basic_set.run(sequence)
            mutex.release()
        except:
            logging.error("error detected") 
          
        time.sleep(random.randint(BASIC_SET_TASK_DELAY_MIN, BASIC_SET_TASK_DELAY_MAX))  
        
#
# Supervision Task
#
def ztask_supervision(mutex):

    logging.info('get_supervision started')
        
    sequence = 0
    while(True):
        
        sequence += 1
        if(sequence > 32):
            sequence = 0
        
        try:
            mutex.acquire(timeout=SUPERVISION_TASK_DELAY_MAX)
            supervision.run(sequence)
            mutex.release()
        except:
            logging.error("error detected") 
         
        time.sleep(random.randint(SUPERVISION_TASK_DELAY_MIN, SUPERVISION_TASK_DELAY_MAX))
    

#
# Main entry point
#                   
if __name__ == '__main__':
                    
    logging.basicConfig(filename= fr'./{datetime.datetime.now().strftime("%Y-%m-%d %H%M%S")}-z-wave-serial-api-test.log',
                    filemode='a',
                    format='%(asctime)s.%(msecs)03d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)
       
    #create mutex
    shared_mutex= threading.Lock()
    
    #created the Thread & start it
    t1 = threading.Thread(target=ztask_basic_set, args=(shared_mutex,))
    t1.start()
    
    #created the Thread & start it
    t2 = threading.Thread(target=ztask_supervision, args=(shared_mutex,))
    t2.start()

    #Joined the threads. this should not 
    t1.join()
    t2.join()
    