from debug import debug
from protocol import *

MODULE = "I2C"
LEVEL = 3
LEVEL_DETAIL = 4

class I2CComm():
  # def __init__(self):

  def send(self, address, data=[], boardid = 200):
    DATA_LEN = 3
    if len(data) > DATA_LEN:
      raise Exception(f'This command accepts address and {DATA_LEN} bytes of data')
    
    # Construct frame
    out = [len(data)]
    out.append(address)
    out += data
    for x in range(DATA_LEN - len(data)):
      out.append(0xff) # Padding
    out.append(boardid)

    debug(f'.send {out}', MODULE, LEVEL)
    
    # Send to protocol
    command = Protocol.I2CCommandSend
    command.send(out)

  def read(self, address, data, read_len, boardid = 0):

    command = Protocol.I2CReadData
    out = [33]
    out += data
    out.append(boardid)
    
    debug(f'.read {out}', MODULE, LEVEL)
    
    command.send(out)
    data = command.receive(read_len)
    debug(f'Read data {data}', MODULE, LEVEL_DETAIL)
    return data

if __name__ == "__main__":
  test = I2CComm()
  test.send(20, [], boardid = 0) # Device, list of data to device
  test.read(33, [19], read_len = 1, boardid = 0)
