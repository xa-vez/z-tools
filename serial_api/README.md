# Serial API Test
## _Simple Z-Wave Test using Python3_  
Creation Date: 2023-11-16th
Version: 1.0.0.b (beta)

## Requirements

- Python 3.11 Linux, Windows (Tested) 
- Python 3.5 RPi (Tested) 
- pyserial (apt install python3-serial or pip3 install pyserial)
- Z-Wave Network preconfigured \
-- Z-Wave Controller : Node 1 \
-- Z-Wave Device_1 : Node 2 (This device can be used to route frames) \
-- Z-Wave Device_2 : Node 3 (This device can be reached by Node 2) \
-- Z-Wave Device_3 : Node 4 \
-- Z-Wave Device_N : Node N

## Configuration

- Configure hw/zserial.py serial port ("/dev/ttyACMxx" for Linux or "COMxx" for Windows) 
- User can change destination Node Id 'DD' into the sources \
-- CMD_BASIC_SET_ON=(b'\x0f\x00\xa9\x01\xDD\x03\x20\x01\x01\x25\x00\x00\x00\x00') \
-- CMD_SUPERVISION=(b'\x0f\x00\xa9\x01\xDD\x03\x6c\x01\xff\x25\x00\x00\x00\x00') 

> (ZIP) send "(unknown) [d867cdd6-0007-000]" COMMAND_CLASS_SUPERVISION SUPERVISION_GET 0E 042501FF00 

> 2023-10-26T16:02:27.670274+0100 W 01 0f 00 a9 0a 08 03 6c 01 13 25 00 00 00 00 28 2b \
> 2023-10-26T16:02:27.676743+0100 R 06 01 04 01 a9 01 52 \
> 2023-10-26T16:02:27.677084+0100 W 06 \
> 2023-10-26T16:02:27.711764+0100 R 01 1d 00 a9 28 00 00 03 01 d4 ce 7f 7f 7f 00 00 02 07 00 00 00 03 01 00 00 7f 7f 7f 7f 7f 7c \
> 2023-10-26T16:02:27.712166+0100 W 06 \
> 2023-10-26T16:02:27.739015+0100 R 01 0e 00 a8 00 0a 08 05 6c 02 13 00 00 00 d4 f7 \
> 2023-10-26T16:02:27.739397+0100 W 06 

## Lauch

- User can run each test using: \
-- $ python3 cmd_basic_set.py \
-- $ python3 cmd_supervision.py

- User can run all tests using: \
-- $ python3 ztest.py (default arguments) \
-- $ python3 ztest.py -t serial -p /dev/ttyACM0 -s 1 -d 3 

## Protocol 
https://sdomembers.z-wavealliance.org/wg/Members/document/previewpdf/1769

(Byte 0) SOF \
(Byte 1) length : from length to cs \
(Byte 2) type : 0-> request 1->response (all other values are reserved) \
(Byte 3) Command ID N bytes \
(Byte 3+n) Command Payload \
(Byte 3+n+1) CS \

CMD_ON=(b'\x0f\x00\xa9\x01\xDD\x03\x20\x01\x01\x27\x00\x00\x00\x00')

0x01 : Start of Frame (to be concatenated) \
0x0f : lenth \
0x00 : type->request \
0xa9 : Bridge Controller Node Send Data Command \
    x01\x0a\x03\x20\x01\x01\x27\x00\x00\x00\x00' : Payload Command \
    
    0x01: Source node Id \
    0xDD: Destination node Id \
    0x03: Data Length \
            
    0x20:  \
    0x01:  \
    0x01: ON  \

0x27: Tx Options \
    7bit:Reserved \
    6bit:Reserved \
    5bit:Enable Explore NPDUs *** \
    4bit:Disable Routing \
    3bit:Reserved \
    2bit:Enable Automatic Routing *** \
    1bit:Transmit with low power \
    0bit:TMPDU Acknowledgment request *** \

0x00\0x00\0x00\0x00 : Route  \
0xXX: Session Identifier  (to be concatenated) \
0xYY: Checksum  (to be concatenated) \
