from debug import debug # Debug options
from serial_connection import Serial_Comm

MODULE = "PROTOCOL"
LEVEL = 3
LEVEL_DETAIL = 4

# Static for now
comm = Serial_Comm()

class Command():
  def __init__(self, name, address, data_len = 0, read = False):
    self.cmd = address
    self.data_len = data_len
    self.read = read
    self.name = name

  def send(self, data=[]):
    if len(data) != self.data_len:
      raise Exception(f'This command needs {self.data_len} bytes of data, not {len(data)}')
    
    debug(f'{self.name}.send', MODULE, LEVEL)
    debug(f'cmd:{self.cmd}, data_len:{self.data_len}, read:{self.read}, data: {data}', MODULE, LEVEL_DETAIL)
    
    out = [self.cmd]
    out += data
    comm.write(out)
    return
  
  def receive(self, data_len):
    if self.read == False:
      raise Exception(f'This command expects no data from board')
    
    data = comm.read(data_len)
    return data


class CommandRange():
  def __init__(self, name, addrL, addrH, data_len = 0, read = False):
    self.addrL = addrL
    self.addrH = addrH
    self.data_len = data_len
    self.read = read
    self.name = name 

  def send(self, boardid, data = []):
    if len(data) !=  self.data_len:
      raise Exception(f'This command needs board id and {self.data_len} bytes of data')
    
    cmd = self.addrL + boardid
    if cmd > self.addrH:
      raise Exception(f'Boardid is out of bounds ({self.addrL},{self.addrH})')

    debug(f'{self.name}.send', MODULE, LEVEL)
    debug(f'addrL:{self.addrL}, addrH:{self.addrH}, read:{self.read}, boardid; {boardid}, data: {data}', MODULE, LEVEL_DETAIL)
    
    # Add command to queue
    out = [cmd]
    out += data
    comm.write(out)
    return
  
  def receive(self, data_len):
    if self.read == False:
      raise Exception(f'This command expects no data from board')
    
    recv = []
    return recv


class Protocol():
  BoardDefineID = CommandRange('BoardDefineID', 0, 9)
  BoardEventSendData = CommandRange('BoardEventSendData', 10, 19, read=True)
  BoardIsLast = CommandRange('BoardIsLast', 20, 29)
  BoardActivate = CommandRange('BoardActivate', 30, 39)
  TriggerArm = Command('TriggerArm', 100)
  TriggerRoll = Command('TriggerRoll', 101)
  TriggerRollNot = Command('TriggerRollNot', 102)
  ADCSlowSamplesSend = CommandRange('ADCSlowSamplesSend', 110, 119, read=True)
  ADCSlowSamplesConf = Command('ADCSlowSamplesConf', 120, 2)
  TriggerPoint = Command('TriggerPoint', 121, 2)
  ADCFastSamplesConf = Command('ADCFastSamplesConf', 122, 2)
  ADCFastSamplesSkip = Command('ADCFastSamplesSkip', 123, 1)
  ADCTimebase = Command('ADCTimebase', 124, 1)
  SerialWaitConf = Command('SerialWaitConf', 125, 1)
  ScreenMiniDraw = Command('ScreenMiniDraw', 126, 1)
  TriggerTreshold = Command('TriggerTreshold', 127, 1)
  TriggerType = Command('TriggerType', 128, 1)
  TriggerHold = Command('TriggerHold', 129, 2)
  TriggerChannelToggle = Command('TriggerChannelToggle', 130, 1)
  SPICommandSend = Command('SPICommandSend', 131, 2)
  DelayCounterRecv = Command('DelayCounterRecv', 132, read=True)
  CarryCounterRecv = Command('CarryCounterRecv', 133, read=True)
  GainToggle = Command('GainToggle', 134, 1)
  SerialDelayTimerConf = Command('SerialDelayTimerConf', 135, 2)
  I2CCommandSend = Command('I2CCommandSend', 136, 6)
  DataOutputPathToggle = Command('DataOutputPathToggle', 137, 1)
  ADCLockInSamplesShift = Command('ADCLockInSamplesShift', 138, 2)
  TriggerAutoArmToggle = Command('TriggerAutoArmToggle', 139)
  TriggerRuntTreshold = Command('TriggerRuntTreshold', 140)
  OversamplingChannelToggle = Command('OversamplingChannelToggle', 141, 1)
  UniqueIDRecv = Command('UniqueIDRecv', 142, read=True)
  HighResModeToggle = Command('HighResModeToggle', 143)
  ExternalTriggerPinToggle = Command('ExternalTriggerPinToggle', 144)
  ChannelSelectRecvData = Command('ChannelSelectRecvData', 145, 1)
  I2CReadData = Command('I2CReadData', 146, 3, read=True)
  FirmwareVersionRecv = Command('FirmwareVersionRecv', 147, read=True)

if __name__ == '__main__':
  # print(f"{Protocol}")
  # for var in vars(Protocol):
  #   print(f"{var}")

  #
  # Test class Command
  #
  command = Protocol.SPICommandSend
  try: 
    command.send([0, 0, 0]) # Should raise exception
  except Exception as error:
    print('1. Caught this error: ' + repr(error))

  try: 
    command.send() # Should raise exception
  except Exception as error:
    print('2. Caught this error: ' + repr(error))

  command.send([0, 0])

  try: 
    command.receive() # Should raise exception
  except Exception as error:
    print('3. Caught this error: ' + repr(error))
  
  #
  # Test class CommandRange
  #
  command = Protocol.BoardDefineID
  try: 
    command.send(1, [1]) # Should raise exception
  except Exception as error:
    print('4. Caught this error: ' + repr(error))

  try:
    command.send(10) # Should raise exception
  except Exception as error:
    print('5. Caught this error: ' + repr(error)) 
  
  command.send(1)

  try:
    command.receive() # Should raise exception
  except Exception as error:
    print('6. Caught this error: ' + repr(error)) 

  command = Protocol.BoardEventSendData
  command.receive()

  print("ok")
