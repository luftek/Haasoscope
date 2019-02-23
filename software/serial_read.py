from serial import Serial
from struct import unpack
import time

ser=Serial("COM16",1500000,timeout=1.0)
waitlittle = 0.1 #seconds
LENGTH = 40

#This is a _minimal_ set of example commands needed to send to a board to initialize it properly
commands = [
    # Board selection, FPGA var setting
    [0],   # Set first board id to 0
    [20],  # Board is last board
    [30],  # Select board 0 as active
    [135, 0, 100], #serialdelaytimerwait of 100
    [122, LENGTH>>8, LENGTH&0xff],  #number of samples 10
    [123, 0], #send increment
    [124, 3], #downsample 3
    [125, 1], #tickstowait 1

    # ADC on, IOExpanders, I2C
    [136, 2, 0x20, 0x00,    0, 255, 200], # io expanders on (!)
    [136, 2, 0x20, 0x01,    0, 255, 200], # io expanders on (!)
    [136, 2, 0x21, 0x00,    0, 255, 200], # io expanders on (!)
    [136, 2, 0x21, 0x01,    0, 255, 200], # io expanders on (!)
    [136, 2, 0x20, 0x12, 0xf0, 255, 200], # init
    [136, 2, 0x20, 0x13, 0x0f, 255, 200], # init (and turn on ADCs!)
    [136, 2, 0x21, 0x12,    0, 255, 200], # init
    [136, 2, 0x21, 0x13,    0, 255, 200], # init

    # ADC, SPI Init
    [131, 8,  0], # adc offset
    # [131, 6, 16], #offset binary output
    [131, 6, 80], #test pattern output

    # ADC, SPI Init
    [131, 4, 36], #300 Ohm termination A
    [131, 5, 36], #300 Ohm termination B
    [131, 1,  0], #not multiplexed

    # DAC init, I2C, (# Single Write Command, Figure 5-10)
    [136, 3, 0x60, 80, 136, 22, 0], # channel 0,
    [136, 3, 0x60, 82, 136, 22, 0], # channel 1 
    [136, 3, 0x60, 84, 136, 22, 0], # channel 2 
    [136, 3, 0x60, 86, 136, 22, 0], # channel 3 
]

for command in commands:
    ser.write(command)
    time.sleep(waitlittle)

# OK, we're set up! Now we can read events and get good data out.
ser.write([100, 10]) # arm trigger and get an event
result = ser.read(LENGTH*4)
result = list(result)
if len(result) == LENGTH*4:
  for i in range(0,4):
      print(result[ LENGTH*i : LENGTH*i + LENGTH]) # print out the 4 channels

ser.close()
