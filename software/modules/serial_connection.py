from debug import debug # Debug options

MODULE = "UART"
LEVEL = 3
LEVEL_DETAIL = 4

from serial import Serial, SerialException

class Serial_Comm():
  
  def __init__(self):
    bitrate = 1500000
    port = "COM16"
    timeout = 3.0
    self.serial = Serial(port,bitrate,timeout=timeout,stopbits=2)
    self.serial.write([0, 20]) #Set board id to 0
    self.serial.write([135, 0, 100]) #serialdelaytimerwait of 100

  def write(self, data):
    debug(f'.write {data}', MODULE, LEVEL_DETAIL)
    self.serial.write(data)

  def read(self, read_len):
    read = self.serial.read(read_len)
    debug(f'.write {read}', MODULE, LEVEL_DETAIL)
    return read

if __name__ == 'main':
  serial = Serial_Comm()
  serial.write([0, 1, 2, 3])