from serial import Serial
from struct import unpack
import time

serialtimeout=0.5
ser=Serial("COM16",1500000,timeout=serialtimeout)
waitlittle = .1 #seconds

#This is a _minimal_ set of example commands needed to send to a board to initialize it properly
commands = [
    [0],   # Set first board id to 0
    [20],  # Board is last board
    [135, 0, 100], #serialdelaytimerwait of 100
    [122, 0, 10],  #number of samples 10
    [123, 0], #send increment
    [124, 3], #downsample 3
    [125, 1], #tickstowait 1
    [136, 2, 0x20, 0x00,    0, 255, 200], # io expander 1A on - use as outputs
    [136, 2, 0x20, 0x01,    0, 255, 200], # io expander 1B on - use as outputs
    [136, 2, 0x21, 0x00,    0, 255, 200], # io expander 2A on - use as outputs
    [136, 2, 0x21, 0x01, 0xff, 255, 200], # io expander 2B on - use as inputs !
    [136, 2, 0x20, 0x12, 0xf0, 255, 200], # init
    [136, 2, 0x20, 0x13, 0x0f, 255, 200], # init (and turn on ADCs!)
    [136, 2, 0x21, 0x12,    0, 255, 200], # init
    [136, 2, 0x21, 0x13, 0xf0, 255, 200], # io expander 2B enable pull-up resistors!
]

for command in commands:
    ser.write(bytearray(command))
    time.sleep(waitlittle)

#request the unique ID
_start=time.time()
ser.write([142]) 
result = ser.read(8)
if len(result) < 8:
  print('serial timeout')
else:  
  uniqueID = ''
  for x in result:
    uniqueID += f'{x:02x}'
  diff = (time.time()-_start)
  print(f'uniqueID: 0x{uniqueID} in {diff:6.3f} s')

#request the firmware version
_start=time.time()
ser.write([147]) 
result = ser.read(1)
if len(result) > 0:
  fw = result[0]
else:
  fw = 0
  print('serial timeout')
diff = (time.time()-_start)
print(f'fw: {fw} in {diff:6.3f} s')

_start=time.time()
for i in range(2):
    reg = 0x12 + i
    ser.write([146, 0x21, reg, 0]) #request the IO expander data from 2B for board 0
    result = ser.read(1)
    if len(result) > 0: 
        print(f'reg: 0x{reg:02x}, val: 0x{result[0]:02x}')
diff = diff = (time.time()-_start)
print(f'got i2c data in {diff:6.3f} s')

ser.close()
