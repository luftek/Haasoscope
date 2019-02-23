from debug import debug # Debug options

MODULE = "UART"
LEVEL = 3
LEVEL_DETAIL = 4

from serial import Serial, SerialException

class Serial_Comm():
  
  def __init__(self):
    bitrate = 1500000
    port = "COM16"
    timeout = 1.0
    self.serial = Serial(port,bitrate,timeout=timeout,stopbits=2)
    commands = [
      # Board selection, FPGA var setting
      [0],   # Set first board id to 0
      [20],  # Board is last board
      [30],  # Board 0 is active
    ]
    for command in commands:
      self.serial.write(command)

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