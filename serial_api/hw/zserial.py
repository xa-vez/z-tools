#!/usr/bin/python3

import binascii
import datetime
import logging 
import serial

#
# Serial Port Class
#
class zSerial:
   
    def __init__(self, serial="/dev/ttyACM0", baudrate=115200):
        self.ser = ''
        self.port = serial
        self.baudrate = baudrate

    def Flush(self):
        self.ser.flushInput()
        self.ser.flushOutput()
        
    def Open(self):
        self.ser = serial.Serial(self.port, self.baudrate, timeout=0.05)        
        self.ser.setRTS(False)
    
    def Close(self):
        self.ser.setRTS(True)
        self.ser.close()
    
    def ReadAll(self):
        data = self.ser.readall()  
        return data
    
    def SendCommand(self, command):
        print(str(datetime.datetime.now(datetime.timezone.utc).isoformat()) + ' W ' + binascii.hexlify(command, ' ').decode('utf-8'))
        logging.debug('W ' + binascii.hexlify(command).decode('utf-8'))
        self.ser.write(command)  
    
    def ReadResponse(self):
        data = self.ReadAll()  
        print(str(datetime.datetime.now(datetime.timezone.utc).isoformat()) + ' R ' + binascii.hexlify(data, ' ').decode('utf-8'))
        logging.debug('R ' + binascii.hexlify(data).decode('utf-8'))
        return data
    
