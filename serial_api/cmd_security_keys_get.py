#!/usr/bin/python3

import datetime
import logging
import random
import time

from hw.zserial import *

KEY_GET_DELAY_MIN = 4
KEY_GET_DELAY_MAX = 5

KEYS_READ_CMDS = {
                    "S0"  : b'\x06\x00\x23\x00\x2d\x10',
    "S2_UNAUTHENTICATED"  : b'\x06\x00\x23\x00\x55\x10',
    "S2_AUTHENTICATED"    : b'\x06\x00\x23\x00\x65\x10',
    "S2_ACCESS"           : b'\x06\x00\x23\x00\x75\x10',
    "S2_AUTHENTICATED_LR" : b'\x06\x00\x23\x00\xA5\x10',
    "S2_ACCESS_LR"        : b'\x06\x00\x23\x00\xB5\x10'
}

# ACK 
ACK=(b'\x06')
# SOF 
SOF=(b'\x01')

#
# Security Keys Get Class
#
class security_keys_get:
       
    def __init__(self):
        pass
    
    def run():

        #serial port instance
        ser = zSerial()
        
        cmd=''
        res=''

        logging.debug('===============' + ' Get KEYS ' + '========================')
        for key in KEYS_READ_CMDS:

            cmd = KEYS_READ_CMDS[key] 

            logging.debug('Command ' + key )
            cmd=bytearray(cmd)
    
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
                else: 
                    logging.error("***** ERROR (1) ACK command not received *****")
                    
            except:
                logging.error(">>> device busy !")
                
            ser.Close()
        
       
#
# Main entry point
#    
if __name__ == "__main__":
                                                           
    logname = '%s-z-wave-serial-api-security-keys-get.log' % datetime.datetime.now().strftime("%Y-%m-%d %H%M%S")
    logging.basicConfig(
            filename=logname,
            format='%(asctime)s.%(msecs)03d %(name)s %(levelname)s %(message)s',
            datefmt='%H:%M:%S',
            level=logging.DEBUG)

    while(True):
        
        # run test
        security_keys_get.run()
        
        # sleep for a while
        time.sleep(random.randint(KEY_GET_DELAY_MIN, KEY_GET_DELAY_MAX))
