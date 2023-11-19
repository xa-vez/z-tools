#!/usr/bin/python3

import datetime
import logging
import random
import time
import sys
import os

from hw.zserial import *

SUPERVISION_DELAY_MIN = 4
SUPERVISION_DELAY_MAX = 5

# supervision 
CMD_SUPERVISION=(b'\x0f\x00\xa9\x01\xDD\x03\x6c\x01\xff\x27\x00\x00\x00\x00')
# ACK 
ACK=(b'\x06')
# SOF 
SOF=(b'\x01')

#
# Supervision Class
#
class supervision:

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
        if(self.transport == supervision.TRANSPORT_SERIAL):
            interface = zSerial(self.port)
        elif(self.transport == supervision.TRANSPORT_TCP):
            print("not implemented")
        else:
            print("error")
            quit()
                
        cmd=''
        res=''
        
        logging.debug('=================== Session Identifier : ' + str(session_identifier) + ' =====================')                      
        logging.debug('Command Supervision')
        cmd=bytearray(CMD_SUPERVISION)
        
        # insert source and destination
        cmd[3] = self.source   
        cmd[4] = self.destination 

        #insert session_identifier
        cmd[8] = session_identifier
            
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
                    time.sleep(.2)
                    res = interface.ReadResponse()          
                    l = len(res)
                    if(l > 0):
                        interface.SendCommand(ACK) 
                    else:
                        logging.error("***** ERROR (3) Supervision Report not received *****")
                else:
                    logging.error("***** ERROR (2) ACK protocol not received *****")
            else:
                logging.error("***** ERROR (1) ACK command device not received *****")
        except:
            logging.error(">>> device busy")        
        
        interface.Close()

   
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
    
    sup = supervision()
    
    session = 0
    while(True):
        
        session += 1
        if(session > 32):
            session = 0
            
        # run test
        sup.run(session)
        
        # sleep for a while
        try:
            time.sleep(random.randint(SUPERVISION_DELAY_MIN, SUPERVISION_DELAY_MAX))
        except KeyboardInterrupt:
            try:
                sys.exit(130)
            except SystemExit:
                os._exit(130)

        
