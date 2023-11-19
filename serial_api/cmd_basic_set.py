#!/usr/bin/python3

import datetime
import logging
import random
import time
import sys
import os

from hw.zserial import zSerial

BASIC_SET_DELAY_MIN = 4
BASIC_SET_DELAY_MAX = 5
   
# basic set ON
CMD_ON=(b'\x0f\x00\xa9\x01\xDD\x03\x20\x01\x01\x27\x00\x00\x00\x00')
# basic set OFF 
CMD_OFF=(b'\x0f\x00\xa9\x01\xDD\x03\x20\x01\x00\x27\x00\x00\x00\x00')
# ACK 
ACK=(b'\x06')
# SOF 
SOF=(b'\x01')

#
# Basic Set Class
#
class basic_set:
       
    TRANSPORT_SERIAL = "serial"
    TRANSPORT_TCP = "tcp"

    def __init__(self, transport="serial", 
                 port="/dev/ttyACM0", 
                 source=1, 
                 destination=2):
        self.transport = transport
        self.port = port
        self.source = source
        self.destination = destination 

    def run(self, session_identifier=0):

        #serial port instance
        if(self.transport == basic_set.TRANSPORT_SERIAL):
            interface = zSerial(self.port)
        elif(self.transport == basic_set.TRANSPORT_TCP):
            print("not implemented")
        else:
            print("error")
            quit()
        
        cmd=''
        res=''
            
        logging.debug('=================== Session Identifier : ' + str(session_identifier) + ' =====================')

        if(session_identifier%2 != 0):    
            logging.debug('Command On')
            cmd=bytearray(CMD_ON)
        else:
            logging.debug('Command Off')
            cmd=bytearray(CMD_OFF)
    
        # insert source and destination
        cmd[3] = self.source   
        cmd[4] = self.destination   

        #insert session identifier 
        cmd.append(session_identifier)
    
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
            interface.Open()
            interface.SendCommand(msg)        
            res = interface.ReadResponse()
            l = len(res)
            if(l > 0):
                interface.SendCommand(ACK)            
                res = interface.ReadResponse()          
                l = len(res)
                if(l > 0):
                    interface.SendCommand(ACK)
                else: 
                    logging.error("***** ERROR (2) ACK protocol not received *****")
            else: 
                    logging.error("***** ERROR (1) ACK command not received *****")
                    
        except:
            logging.error(">>> device busy !")
                
        interface.Close()
        
       
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

    bs = basic_set()

    session = 0
    while(True):
        
        session += 1
        if(session > 15):
            session = 0
        
        # run test
        bs.run(session)
        
        # sleep for a while
        try:
            time.sleep(random.randint(BASIC_SET_DELAY_MIN, BASIC_SET_DELAY_MAX))
        except KeyboardInterrupt:
            try:
                sys.exit(130)
            except SystemExit:
                os._exit(130)