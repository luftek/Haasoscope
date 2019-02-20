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
    return

  def write(self, data):
    debug(f'.write: Address 0x{self.address:02x}, Board id {self.boardid}, Write {data}', MODULE, LEVEL)
    self.i2c.send(self.address, data, self.boardid)

  def read(self, data, read_len):
    debug(f'.read: Address 0x{self.address:02x}, Board id {self.boardid}, Read {data}', MODULE, LEVEL)
    self.i2c.read(self.address,[19], 1, self.boardid)


if __name__ == '__main__':
  import time

  ioexpander = IOExpander(address = 0x21, boardid = 0)
  ioexpander.write([0x00, 0x00]) # GPIOA Output
  ioexpander.write([0x01, 0x00]) # GPIOB Output

  # Turn LEDs on/off
  while True:
    ioexpander.write([0x12, 0x0a])
    time.sleep(0.25)
    ioexpander.write([0x12, 0x05])
    time.sleep(0.25)