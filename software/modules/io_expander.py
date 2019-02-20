from debug import debug
from i2c import I2CComm

MODULE = "IO_EXPANDER"
LEVEL = 2
LEVEL_DETAIL = 4

"""\
    Driver for IO Expanders, Microchip MCP23017
    http://ww1.microchip.com/downloads/en/DeviceDoc/20001952C.pdf

    We should implement:
    - output/input register
    - output set
    - input read?
"""

class IOExpander():
  def __init__(self, address, boardid = 0):
    self.address = address
    self.boardid = boardid
    self.i2c = I2CComm()

  def write(self, data):
    debug(f'.write: Address 0x{self.address:02x}, Board id {self.boardid}, Write {data}', MODULE, LEVEL)
    self.i2c.send(self.address, data, self.boardid)

  def read(self, reg):
    read = self.i2c.read(self.address, reg, 1, self.boardid)
    debug(f' .read: Address 0x{self.address:02x}, Board id {self.boardid}, Read  {[reg, read]}', MODULE, LEVEL)
    return read

if __name__ == '__main__':
  import time

  ioexpander = IOExpander(address = 0x21, boardid = 0)
  ioexpander.write([0x00, 0x00]) # GPIOA Output
  ioexpander.write([0x01, 0x00]) # GPIOB Output

  # Turn LEDs on/off
  for x in range(10):
    ioexpander.write([0x12, 0x0a])
    time.sleep(0.25)
    ioexpander.write([0x12, 0x05])
    time.sleep(0.25)

  # Display all registers from ioexpander
  for x in range(0x16):
    read = ioexpander.read(x)
    print("[0x{:02x}, 0x{:02x}]".format(x, read))

  # Read how FPGA is changing LEDs
  while True:
    reg = 0x12
    read = ioexpander.read(reg)
    print("[0x{:02x}, 0x{:02x}]".format(reg, read))
    time.sleep(0.2)
  