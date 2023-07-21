import serial
import time
import serial.tools.list_ports

'''
ports = serial.tools.list_ports.comports()
portList = []
for port, desc, hwid in sorted(ports):
     portList.append(port)
     # print("{}: {} [{}]".format(port, desc, hwid))
'''

class WAVEGEN:

    def __init__(self, port):
        self.port = port
        
        self.states = [0,0]
        
        self.waveType = [0,0]
        # Create an array that lists the names of the various wave types
        self.waveTable = ["Sine", "Square", "Pulse", "Triangle", "Slope",
                          "CMOS", "DC Level", "Partial Sine Wave", "Half Wave",
                          "Full Wave", "Posative Ladder Wave", "Negative Ladder Wave",
                          "Posative Trapezoidal Wave", "Negative Trapezoidal Wave",
                          "Noise", "Index Rise", "Index Fall", "Logarithmic Rise",
                          "Logarithmic Fall", "Sinker Pulse", "Multi-Audio", "Lorenz"]
        
        self.modTypes = ["AM", "FM", "PM", "ASK", "FSK", "PSK", "PULSE", "BURST"]
        
        self.freq = [0,0]
        self.amplitude = [0,0]
        self.offset = [0,0]
        self.dutyCycle = [0,0]
        self.phase = [0,0]

        self.modType = [10,10]

        self.serial_connection(self.port)


    #Initialize Serial Port
    def serial_connection(self, port):
        self.ser = serial.Serial()
        self.ser.baudrate = 115200 
        self.ser.port = port

        #check to see if port is open or closed
        if (self.ser.isOpen() == False):
            print ('The Port is Open ' + self.ser.portstr)
            #timeout in seconds
            self.ser.timeout = 10
            self.ser.open()

        else:
            print ('The Port is Closed ' + self.ser.portstr)

    def serialWrite(self, command):
        self.toSend = (':w{}.\x0a\x0a'.format(command)).encode()
        self.ser.write(self.toSend)
        self.response = self.ser.readline().split(b'.')[0]
        # Ensures command was ackowledge by function generator
        self.expectedResponse = b':ok'
        print('Sending: {}'.format(self.toSend))
        if self.response == self.expectedResponse:
            print('Command acknowledged by device')
        else:
            print('serialWrite | ERROR: Failed to recieve acknowledgement from device for command: {}'.format(self.toSend))
    
    def serialRead(self, readCode):
        if 0 <= readCode <= 86: # readCode range
            prefix =':r{}'.format(readCode)
            toSend =('{}=0.\x0a\x0a'.format(prefix)).encode()
            self.ser.write(toSend)
            recieve = (self.ser.readline()).split(b'=')
            if prefix.encode() == (recieve[0]):
                output = (recieve[1].split(b'.'))[0]
                return output
    # state setter and getter

    '''
    Setter and getter for state of the function generator channels
    '''
    def getStates(self):
        self.readOut = (self.serialRead(10)).split(b',')
        self.states[0] = int(self.readOut[0])
        self.states[1] = int(self.readOut[1])
        return self.states
    def setState(self, reqState, chNo):


        if 0 <= reqState <= 1:
            self.getStates()
            if chNo == 1:
                self.newStateCh1 = reqState
                self.newStateCh2 = self.states[1]
                self.stateSend = '10={},{}'.format(self.newStateCh1, self.newStateCh2)
                self.serialWrite(self.stateSend)
            elif chNo == 2:
                self.newStateCh1 = self.states[0]
                self.newStateCh2 = reqState
                self.stateSend = '10={},{}'.format(self.newStateCh1, self.newStateCh2)
                self.serialWrite(self.stateSend)
    '''
    Setter and getter for wave type of the function generator channels
    '''
    def getWaveTypes(self):
        self.waveCh1 = int(self.serialRead(11))
        self.waveCh2 = int(self.serialRead(12))
        self.waveType = [self.waveCh1, self.waveCh2]

        return self.waveType
    def setWaveType(self, wave, chNo):
        self.offset = chNo - 1
        self.cmdPrefix = 11 + self.offset
        self.command = '{}={}'.format(self.cmdPrefix, wave)
        self.serialWrite(self.command)
    '''
    Setter and getter for frequency of the function generator channels
    '''      
    def getFreq(self):
        self.freqCh1 = int(self.serialRead(13))
        self.freqCh2 = int(self.serialRead(14))
        self.freq = [self.freqCh1, self.freqCh2]
        return self.freq
    def setFreq(self, freq, multiplier, chNo):
        self.offset = chNo - 1
        self.cmdPrefix = 13 + self.offset
        self.command = '{}={},{}'.format(self.cmdPrefix, freq, multiplier)
        self.serialWrite(self.command)
    
    '''
    Setter and getter for amplitude of the function generator channels
    '''
    def getAmplitude(self):
        self.ampCh1 = int(self.serialRead(15))
        self.ampCh2 = int(self.serialRead(16))
        self.amplitude = [self.ampCh1, self.ampCh2]
        return self.amplitude
    # Aplitude in mV
    def setAmplitude(self, amp, chNo):  
        self.offset = chNo - 1
        self.cmdPrefix = 15 + self.offset
        self.command = '{}={}'.format(self.cmdPrefix, amp)
        self.serialWrite(self.command)

    '''
    Setter and getter for offset of the function generator channels
    Offset setting
        The PC sends: w17=1000. set the offset output of channel 1 to 0v.
        The PC sends: w17=2500. set the offset output of channel 1 to 15v.
        The PC sends: w17=1. set the offset output of channel 1 to -9.99v.
        When setting the offset output of channel 2, just change :w17 to :w18, and the others remain unchanged.
        For example: PC sent: w18=1. set the offset output of channel 2 to -9.99v.
    '''
    def getOffset(self):
        self.offsetCh1 = int(self.serialRead(17))
        self.offsetCh2 = int(self.serialRead(18))
        self.offset = [self.offsetCh1, self.offsetCh2]
        return self.offset   
    def setOffset(self, offset, chNo):
        self.offset = chNo - 1
        self.cmdPrefix = 17 + self.offset
        self.command = '{}={}'.format(self.cmdPrefix, offset)
        self.serialWrite(self.command)

    '''
    Setter and getter for duty cycle of the function generator channels
    '''
    def getDutyCycle(self):
        self.dutyCycleCh1 = int(self.serialRead(19))
        self.dutyCycleCh2 = int(self.serialRead(20))
        self.dutyCycle = [self.dutyCycleCh1, self.dutyCycleCh2]
        return self.dutyCycle
    def setDutyCycle(self, dutyCycle, chNo):
        self.offset = chNo - 1
        self.cmdPrefix = 19 + self.offset
        self.command = '{}={}'.format(self.cmdPrefix, int(dutyCycle*100))
        self.serialWrite(self.command)

    '''
    Setter and getter for phase of the function generator channels
    '''
    def getPhase(self):
        self.phaseCh1 = int(self.serialRead(21))
        self.phaseCh2 = int(self.serialRead(22))
        self.phase = [self.phaseCh1, self.phaseCh2]
        return self.phase
    def setPhase(self, phase, chNo):
        self.offset = chNo - 1
        self.cmdPrefix = 21 + self.offset
        self.command = '{}={}'.format(self.cmdPrefix, int(phase*100))
        self.serialWrite(self.command)
    '''
    Setter and getter for mod type of the function generator channels
    '''
