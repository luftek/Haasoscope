from debug import debug
from i2c import I2CComm

MODULE = "DAC"
LEVEL = 2
LEVEL_DETAIL = 4

"""\
    Driver for DAC, Microchip MCP4728
    http://ww1.microchip.com/downloads/en/DeviceDoc/22187E.pdf

    We should implement:
    - value change
"""

class DAC():
  def __init__(self, boardid = 0):
    self.address = 0x60
    self.boardid = boardid
    self.i2c = I2CComm()

  def value_set(self, channel, value_in_half_mv):
    value = value_in_half_mv
    if value > 0x1fff and value < 0:
        raise ValueError(f'Value {value} is out of range [0,8191]')
    if channel > 3 and channel < 0:
        raise ValueError(f'Channel {channel} is out of range [0,3]')
    
    if value > 0xfff:
        gain = 2
        value = value >> 1
    else:
        gain = 1
    
    valH = (value & 0xff00) >> 8
    valL =  value & 0x00ff

    # Single Write Command, Figure 5-10
    ch_mask = 0x50 | 0x08 | (channel << 1)
    byte_two = 0x80 | valH
    if gain == 2:
      byte_two |= 0x10

    data = [ch_mask, byte_two, valL]

    debug(f'Board id {self.boardid}, Voltage on ch: {channel} is: {value_in_half_mv/2} mV', MODULE, LEVEL)
    self.i2c.send(self.address, data, self.boardid)

if __name__ == '__main__':
  import time

  dac = DAC(boardid = 0)

  # Output voltage sequence 0, 200mV, 400mv,...
  for x in range(17):
    dac.value_set(0, x*200*2)
    time.sleep(2)
