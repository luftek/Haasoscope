from debug import debug
from protocol import Protocol

MODULE = "SPI"
LEVEL = 3
LEVEL_DETAIL = 4

class SPIComm():

  def send(self, reg, value):
    # Construct frame
    out = [reg, value]

    debug(f'.send {out}', MODULE, LEVEL)
    
    # Send to protocol
    command = Protocol.SPICommandSend
    command.send(out)

if __name__ == "__main__":
  import time
  
  """
  #
  # Make sure you run serial_read.py before running this code
  # It will initialize board and all components.
  # SPI commands will then affect output
  #
  """

  spi = SPIComm()
  
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
  
  # Go through list and set value
  for x in mapping:
    val = x[1] | 0b1000
    print(f'{x[0]}V, 0x{val:02x}')

    both_ch = (val << 4) | val
    spi.send(0x08, both_ch)
    time.sleep(3)
