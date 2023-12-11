#!/usr/bin/python3

import datetime
import logging
import random
import time

from hw.zserial import *

KEY_SET_DELAY_MIN = 4
KEY_SET_DELAY_MAX = 5


KEYS_WRITE_CMDS = {
                    "S0"  : b'\x18\x00\x24\x00\x2d\x00\x10\xB1\xC9\x06\x44\x60\x5D\x3C\x5B\x58\xE2\x57\xB9\x96\x3F\x3B\xF2\x00',
    "S2_UNAUTHENTICATED"  : b'\x18\x00\x24\x00\x55\x00\x10\x01\x11\x22\x33\x44\x55\x66\x77\x88\x99\xAA\xBB\xCC\xDD\xEE\xFF\x00',
    "S2_AUTHENTICATED"    : b'\x18\x00\x24\x00\x65\x00\x10\x02\x11\x22\x33\x44\x55\x66\x77\x88\x99\xAA\xBB\xCC\xDD\xEE\xFF\x00',
    "S2_ACCESS"           : b'\x18\x00\x24\x00\x75\x00\x10\x03\x11\x22\x33\x44\x55\x66\x77\x88\x99\xAA\xBB\xCC\xDD\xEE\xFF\x00',
    "S2_AUTHENTICATED_LR" : b'\x18\x00\x24\x00\xA5\x00\x10\x04\x11\x22\x33\x44\x55\x66\x77\x88\x99\xAA\xBB\xCC\xDD\xEE\xFF\x00',
     "S2_ACCES_LR"        : b'\x18\x00\x24\x00\xB5\x00\x10\xB7\xF9\x6C\x63\xCA\xE8\xB7\xF6\xB5\x72\x0a\x2a\x89\x5a\xa5\xc3\x00'
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
        for key in KEYS_WRITE_CMDS:

            cmd = KEYS_WRITE_CMDS[key] 

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
                                                           
    logname = '%s-z-wave-serial-api-security-keys-set.log' % datetime.datetime.now().strftime("%Y-%m-%d %H%M%S")
    logging.basicConfig(
            filename=logname,
            format='%(asctime)s.%(msecs)03d %(name)s %(levelname)s %(message)s',
            datefmt='%H:%M:%S',
            level=logging.DEBUG)

    while(True):
        
        # run test
        security_keys_get.run()
        
        # sleep for a while
        time.sleep(random.randint(KEY_SET_DELAY_MIN, KEY_SET_DELAY_MAX))
