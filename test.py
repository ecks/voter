import time

class StampList:
  def __init__(self):
    self.count = 0
    self.sent = 0
    self.list = []

  def makeStamp(self, checksum, streamID, seqNum):
    return (time.time(), checksum, streamID, seqNum)    

  def appendStamp(self, checksum, streamID, seqNum):
    self.list.append(self.makeStamp(checksum, streamID, seqNum))
    self.count = self.count + 1

  def getCount(self):
    return self.count

  def isSent(self):
    return self.sent

  def send(self):
    self.sent = 1

  def __repr__(self):
    string = ''
    string = string + ' ' + str(self.count) + ' ' + str(self.sent)
    for stamp in self.list:
      string = string + str(stamp) + '\n'  
    return string

class MessageStamp:
  def __init__(self):
    self.dups = {} 

  def addStamp(self, checksum, streamID, seqNum):
    if not seqNum in self.dups:
      self.dups[seqNum] = StampList()
    self.dups[seqNum].appendStamp(checksum, streamID, seqNum)
 
  def getCount(self, seqNum):
    return self.dups[seqNum].getCount()

  def isSent(self, seqNum):
    return self.dups[seqNum].isSent()

  def send(self, seqNum):
    self.dups[seqNum].send()

  def __repr__(self):
    string = ''
    for k,v in self.dups.iteritems():
      string = string + str(k) + ': ' + str(v) + '\n'
    return string

def dataInStreams(streams):
  return all(streams)

fi = open('input_1', 'r')
fo = open('vote', 'w')

streams = []
messageStamps = {}
numOfStreams = 0
for line in fi:
  streams.append(line.split())
  numOfStreams = numOfStreams + 1

while dataInStreams(streams):
  streamID = 0
  for stream in streams:
    head = stream.pop(0)
    if head != 'x':
      checksum = head.split(',')[0]
      seqNum = head.split(',')[1]
      if not checksum in messageStamps:
        messageStamps[checksum] = MessageStamp() 
      messageStamps[checksum].addStamp(checksum, streamID, seqNum)
      if ((float(messageStamps[checksum].getCount(seqNum)) / float(numOfStreams)) > float(1)/float(2)) and not messageStamps[checksum].isSent(seqNum):
        messageStamps[checksum].send(seqNum)
        fo.write(checksum + ',' + seqNum + ' ')
    streamID = streamID + 1

for k,v in messageStamps.iteritems():
  print k,v
