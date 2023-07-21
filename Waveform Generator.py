import serial

#Using  pyserial Library to establish connection
#Global Variables
ser = 0
port = '/dev/tty.usbserial-14130'

#Initialize Serial Port
def serial_connection():
    global ser
    ser = serial.Serial()
    ser.baudrate = 115200 
    ser.port = port

    #check to see if port is open or closed
    if (ser.isOpen() == False):
        print ('The Port is Open ' + ser.portstr)
          #timeout in seconds
        ser.timeout = 10
        ser.open()

    else:
        print ('The Port is Closed ' + ser.portstr)

def setOutput(ch1, ch2):
    # end = '.\x0a\x0a'
    if ((ch1 == 1) or (ch1 == 0) and ((ch2 == 1) or (ch2 == 0))):
        cmd = ':w10={},{}.\x0a\x0a'.format(ch1, ch2)
        toSend = cmd.encode()
        ser.write(toSend)
        out = ser.readline()
        print(out)

    else:
        print('setOutput | ERROR: values of ch1, ch2: {}{}'.format(ch1,ch2))

def setWave(ch, wave):
    if ((ch == 1) or (ch == 2) and (wave <= 256)):
        cmd = ':w1{}={}.\x0a\x0a'.format(ch, wave)
        toSend = cmd.encode()
        ser.write(toSend)
        out = ser.readline()
        print(out)

    else:
        print('setWave | ERROR: values of ch, wave: {}{}'.format(ch, wave))
    
def getState():
    prefix = b':r10'
    cmd = ':r10=0.\x0a\x0a'.encode()
    ser.write(cmd)
    out = ser.readline()
    outsplit =out.split(b'=')

    if outsplit[0] == prefix:
        returnedValue = (outsplit[1].split(b'.'))[0]
        return returnedValue.split(b',')



#call the serial_connection() function
serial_connection()
print(getState())

#setWave(1,3)
#end = '.\x0a\x0a'
#toSend = cmd.encode() + end.encode()
#ser.write(toSend)
#out = ser.read()
#print(out)