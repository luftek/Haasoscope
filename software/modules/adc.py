from debug import debug
from io_expander import IOExpander
from spi import SPIComm
from protocol import Protocol

MODULE = "ADC"
LEVEL = 2
LEVEL_DETAIL = 4

"""\
    Driver for ADC, MAX19506
    https://datasheets.maximintegrated.com/en/ds/MAX19506.pdf

    We should implement:
    - ??
"""

# Common mode bias voltage on pin CMA (0xf0 mask)
# or CMB (0x0f mask)
mapping = (
  ('0.450', 0b111), # This setting does not work on v8.81
  ('0.600', 0b110),
  ('0.750', 0b101),
  ('0.900', 0b100),
  ('1.050', 0b001),
  ('1.200', 0b010),
  ('1.350', 0b011),
)

class ADC():
  def __init__(self, boardid=0):
    self.boardid = boardid
    self.length = 10
    # Init power
    self.io = IOExpander(0x20, self.boardid)
    self.io.write([0x01,0x00]) # Enable GPIOB output on b4, b5

    # self.spi = SPIComm()

  def standby(self, state):
    # HW standby
    if state == True:
      value = 0x30
    else:
      value = 0x00
    self.io.write([0x13, value])

  def set_capture_length(self, length):
    self.length = length
    command = Protocol.ADCFastSamplesConf
    command.send([self.length>>8, self.length&0xff])

  def read_channels(self):
    Protocol.TriggerArm.send()
    command = Protocol.BoardEventSendData
    command.send(self.boardid)
    data = command.receive(self.length * 4)
    return data

if __name__ == '__main__':
  import time
  adc = ADC(boardid = 0)

  # boolean = True
  # for x in range(5):
  #   adc.standby(boolean)
  #   boolean = not boolean
  #   time.sleep(2)

  length = 10
  adc.set_capture_length(length)
  for x in range(5):
    data = adc.read_channels()
    result = list(data)
    if len(result) == length*4:
      for i in range(0,4):
          print(result[ length*i : length*i + length]) # print out the 4 channels
    time.sleep(2)
