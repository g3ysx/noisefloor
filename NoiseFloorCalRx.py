import serial
import time
import datetime

import FT950Config
setRxParams = FT950Config.setRxParams
rxOn        = FT950Config.rxOn
setFreq = FT950Config.setFreq
getRawSM = FT950Config.getRawSM

#Constants
port = 'COM1'
rate = 9600

def setParam(ser, str):
    ser.write(str)
    time.sleep(0.1)

print('NoiseFloor')

#Open and configure serial port
ser = serial.Serial()
ser.baudrate = rate
ser.port = port
ser.open()
print (ser)

# Frequencies  monitored 3.499, 5.258, 6.999, 10.090 and 13.399MHz
freq = ['03499000', '05258000', '06999000', '10090000', '13399000']
print('Starting Initialization')
for f in range (0, len(freq)) :
    setRxParams(ser, freq[f])
print('Initializing complete')

ser.flushInput()
#print('Serial port flushed')

while True:
    mVal = getRawSM(ser)
    print(mVal)
    time.sleep(0.5)
#All done
#close serial port
ser.close()


