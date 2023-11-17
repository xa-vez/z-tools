#!/usr/bin/python3

import datetime
import logging
import random
import time

from hw.zserial import *

BASIC_SET_DELAY_MIN = 4
BASIC_SET_DELAY_MAX = 5
   
# basic set ON
CMD_ON=(b'\x0f\x00\xa9\x01\x0a\x03\x20\x01\x01\x25\x00\x00\x00\x00')
# basic set OFF 
CMD_OFF=(b'\x0f\x00\xa9\x01\x0a\x03\x20\x01\x00\x25\x00\x00\x00\x00')
# ACK 
ACK=(b'\x06')
# SOF 
SOF=(b'\x01')

#
# Basic Set Class
#
class basic_set:
       
    def __init__(self):
        pass
    
    def run(seq=0):

        #serial port instance
        ser = zSerial()
        
        cmd=''
        res=''
            
        logging.debug('=================== Sequence : ' + str(seq) + ' =====================')
           
        if(seq%2 != 0):    
            logging.debug('Command On')
            cmd=bytearray(CMD_ON)
        else:
            logging.debug('Command Off')
            cmd=bytearray(CMD_OFF)
    
        #insert sequence 
        cmd.append(seq)
    
        #insert CRC                
        cs=255
        for c in cmd:
            cs ^= c
    
        cmd.append(cs)
    
        msg = bytearray(SOF)
        msg.extend(cmd)
    
        ####
        #### The packet is complete here
        ####
        try: 
            ser.Open()
            ser.SendCommand(msg)        
            res = ser.ReadResponse()
            l = len(res)
            if(l > 0):
                ser.SendCommand(ACK)            
                res = ser.ReadResponse()          
                l = len(res)
                if(l > 0):
                    ser.SendCommand(ACK)
                else: 
                    logging.error("***** ERROR (2) ACK protocol not received *****")
            else: 
                    logging.error("***** ERROR (1) ACK command not received *****")
                    
        except:
            logging.error(">>> device busy !")
                
        ser.Close()
        
       
#
# Main entry point
#    
if __name__ == "__main__":
                                                           
    logname = '%s-z-wave-serial-api-basic-set.log' % datetime.datetime.now().strftime("%Y-%m-%d %H%M%S")
    logging.basicConfig(
            filename=logname,
            format='%(asctime)s.%(msecs)03d %(name)s %(levelname)s %(message)s',
            datefmt='%H:%M:%S',
            level=logging.DEBUG)

    sequence = 0
    while(True):
        
        sequence += 1
        if(sequence > 15):
            sequence = 0
        
        # run test
        basic_set.run(sequence)
        
        # sleep for a while
        time.sleep(random.randint(BASIC_SET_DELAY_MIN, BASIC_SET_DELAY_MAX))
