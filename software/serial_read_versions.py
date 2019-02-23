from serial import Serial
import time

serialtimeout=0.5
ser=Serial("COM16",1500000,timeout=serialtimeout)
waitlittle = .1 #seconds
board = 0

#This is a _minimal_ set of example commands needed to send to a board to initialize it properly
commands = [
    [0],           # Set first board id to 0
    [20 + board],  # Board is last board
    [135, 0, 100], # serialdelaytimerwait of 100
    [30 + board]   # Select board as active
]

for command in commands:
    ser.write(command)
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

ser.close()
