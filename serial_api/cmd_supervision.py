#!/usr/bin/python3

import datetime
import logging
import random
import time

from hw.zserial import *

SUPERVISION_DELAY_MIN = 4
SUPERVISION_DELAY_MAX = 5

# supervision 
CMD_SUPERVISION=(b'\x0f\x00\xa9\x01\x0a\x03\x6c\x01\xff\x25\x00\x00\x00\x00')
# ACK 
ACK=(b'\x06')
# SOF 
SOF=(b'\x01')

#
# Supervision Class
#
class supervision:

    def __init__(self):
        pass
    
    def run(seq=0):
        
        #serial port instance
        ser = zSerial()
                
        cmd=''
        res=''
        
        logging.debug('=================== Sequence : ' + str(seq) + ' =====================')                      
        logging.debug('Command Supervision')
        cmd=bytearray(CMD_SUPERVISION)
        
        #insert sequence
        cmd[8] = seq
            
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
                    time.sleep(.2)
                    res = ser.ReadResponse()          
                    l = len(res)
                    if(l > 0):
                        ser.SendCommand(ACK) 
                    else:
                        logging.error("***** ERROR (3) Supervision Report not received *****")
                else:
                    logging.error("***** ERROR (2) ACK protocol not received *****")
            else:
                logging.error("***** ERROR (1) ACK command device not received *****")
        except:
            logging.error(">>> device busy")        
        
        ser.Close()

   
#
# Main entry point
#       
if __name__ == "__main__":
                                
    logname = '%s-z-wave-serial-api-supervision.log' % datetime.datetime.now().strftime("%Y-%m-%d %H%M%S")
    logging.basicConfig(
            filename= logname,
            filemode='a',
            format='%(asctime)s.%(msecs)03d %(name)s %(levelname)s %(message)s',
            datefmt='%H:%M:%S',
            level=logging.DEBUG)
    
    sequence = 0
    while(True):
        
        sequence += 1
        if(sequence > 32):
            sequence = 0
            
        # run test
        supervision.run(sequence)
        
        # sleep for a while
        time.sleep(random.randint(SUPERVISION_DELAY_MIN, SUPERVISION_DELAY_MAX))
        
