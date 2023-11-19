#!/usr/bin/python3


import datetime
import threading
import logging
import random
import time
import sys

from cmd_basic_set import *
from cmd_supervision import *


BASIC_SET_TASK_DELAY_MIN = 0
BASIC_SET_TASK_DELAY_MAX = 1

SUPERVISION_TASK_DELAY_MIN = 0
SUPERVISION_TASK_DELAY_MAX = 1

#
# Basic Set Task
#
def ztask_basic_set(mutex, transport, port, source, destination):

    logging.info('get_basic_set started')
    bs = basic_set(transport, port, source, destination)

    session = 0
    while(True):
        
        session += 1
        if(session > 15):
            session = 0
            
        try:
            mutex.acquire(timeout=BASIC_SET_TASK_DELAY_MAX)
            bs.run(session)
            mutex.release()
        except:
            logging.error("error detected") 
          
        try:
            time.sleep(random.randint(BASIC_SET_TASK_DELAY_MIN, BASIC_SET_TASK_DELAY_MAX))
        except:
            quit()

        
#
# Supervision Task
#
def ztask_supervision(mutex, transport, port, source, destination):

    logging.info('get_supervision started')
    sup = supervision(transport, port, source, destination)
   
    sequence = 0
    while(True):
        
        sequence += 1
        if(sequence > 32):
            sequence = 0
        
        try:
            mutex.acquire(timeout=SUPERVISION_TASK_DELAY_MAX)
            sup.run(sequence)
            mutex.release()
        except:
            logging.error("error detected") 
         
        try:
            time.sleep(random.randint(SUPERVISION_TASK_DELAY_MIN, SUPERVISION_TASK_DELAY_MAX))
        except:
            quit()


#
# Main entry point
#                   
if __name__ == '__main__':
    
    import argparse
    
    options = argparse.ArgumentParser(description='Serial log filer. \r\n'
                                                    ' Used to test z-wave network.\n')
    
    options.add_argument('-t', '--transport', 
                        default="serial", 
                        type=str,
                        help='options: tcp, serial')
    
    options.add_argument('-p', '--port', 
                        default="/dev/ttyACM0", 
                        type=str,
                        help='Log COM port')

    options.add_argument('-s', '--source', 
                        default=1, 
                        type=int,
                        help='z-wave source node')

    options.add_argument('-d', '--destination', 
                        default=2, 
                        type=int,
                        help='z-wave destination node')

    options.add_argument('-l', '--logname', 
                        default='%s-z-wave-serial-api.log' % datetime.datetime.now().strftime("%Y-%m-%d %H%M%S") ,
                        type=str,
                        help='z-wave logfile name')

    args = options.parse_args()

    transport = args.transport
    port = args.port
    source = args.source
    destination = args.destination
    logname = args.logname   
    
    logging.basicConfig(
                    filename=logname,
                    filemode='a',
                    format='%(asctime)s.%(msecs)03d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)
        
    #create mutex
    shared_mutex= threading.Lock()
    
    #created the Thread & start it
    t1 = threading.Thread(target=ztask_basic_set, args=(shared_mutex, transport, port, source, destination))
    t1.start()
    
    #created the Thread & start it
    t2 = threading.Thread(target=ztask_supervision, args=(shared_mutex, transport, port, source, destination))
    t2.start()

    #Joined the threads. this should not 
    t1.join()
    t2.join()
    