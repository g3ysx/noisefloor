import serial
import time
import datetime

import FT950Config
setRxParams = FT950Config.setRxParams
rxOn        = FT950Config.rxOn

debug0 = False
debug1 = False #not currently used
debug2 = False
debug4 = False #no sleep to sync to 2min start
debug5 = False #debug samples
debug6 = False #True=single shot

#Constants
port = 'COM1'
rate = 9600
samples = 100

def debugPrint(level,debugStr):
    if ((level==0 and debug0) or
        (level==1 and debug1) or
        (level==2 and debug2) or
        (level==5 and debug5)):
        print('Debug',level,'-',debugStr)
    
def measureNoise():
    while True:
        for f in range (0, len(freq)):
            TF = datetime.datetime.utcnow()
            slpTime = 60*((TF.minute+1)%2) + 60-TF.second - TF.microsecond/1e6
            debugPrint(0,'Sleeping for '+str(slpTime))
            if debug4:
                print('debug not sleeping')
            else:
                time.sleep(slpTime)
            debugPrint(0,'Ready to start at '+str(freq[f])+str(datetime.datetime.utcnow()))

            ustr='FA'+freq[f]+';'
            bstr=bytes(ustr,'ascii')
            ser.write(bstr)
            time.sleep(1)

            readings = [None]*samples
                
            TR = datetime.datetime.utcnow()
            timeReadings = ''
            timeReadings += (str(TR.date())+ ':' +
                           str(TR.hour)+ ':' +
                           str(TR.minute)+ ':' +
                           str(TR.second))
            debugPrint(0,str(timeReadings))
            for i in range (0, samples):
                ser.write(b'SM0;') #get S-Meter
                mStr = bytes(ser.read(size=7))
                mVal = ((int(mStr[3])-ord('0'))*100 +
                        (int(mStr[4])-ord('0'))*10 +
                        int(mStr[5])-ord('0'))
                debugPrint(2,'mStr='+str(mStr)+str(' mval=')+str(mVal))

                readings[i]=mVal;
                debugPrint(5,'sleeping at '+str(timeReadings))
                time.sleep((120.0-5.0)/samples)
                debugPrint(5,'waking at '+str(timeReadings))

            debugPrint(2,str(readings))
            readings.sort()
            debugPrint(2,str(readings))

            print(str(timeReadings) + ' Freq = ' + freq[f] +
                      ' min = ' + str(readings[0]) +
                      ' median = ' + str(readings[int(len(readings)/2)]) +
                      ' max = ' + str(readings[len(readings)-1]))

            if debug6:
                return

# Frequencies  monitored 3.499, 5.258, 6.999, 10.090 and 13.399MHz
freq = ['03499000', '05258000', '06999000', '10090000', '13399000']

print ('NoiseFloor')

#Open and configure serial port
ser = serial.Serial()
ser.baudrate = rate
ser.port = port
ser.open()
debugPrint(0,str(ser))

# Configure RX
rxOn(ser)
for f in range (0, len(freq)) :
    setRxParams(ser, freq[f])

ser.flushInput()
debugPrint(0,'Serial port flushed')

TR = datetime.datetime.utcnow()
debugPrint(0,'TR = '+ str(TR))

# Run test
measureNoise()
#All done
#close serial port
ser.close()


