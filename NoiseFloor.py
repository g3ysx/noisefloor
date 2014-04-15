import serial
import time
import datetime

import FT950Config
setRxParams = FT950Config.setRxParams
rxOn        = FT950Config.rxOn
setFreq = FT950Config.setFreq
getRawSM = FT950Config.getRawSM
getSP = FT950Config.getSP

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

def genFileName():
    fot = datetime.datetime.utcnow()
    smfn = 'Noise-SM-'
    smfn += str(fot)
    smfn = smfn.rsplit('.',1)
    smfn = smfn[0].replace(' ','at')
    smfn = smfn.replace(':','',2)
    smfn += '.txt'
    return (smfn)
    
def measureNoise(smf):
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

            setFreq(ser, freq[f])
            time.sleep(0.9)

            readings = [None]*samples
                
            TR = datetime.datetime.utcnow()
            timeReadings = ''
            timeReadings += (str(TR.date())+ ':' +
                           str(TR.hour)+ ':' +
                           str(TR.minute)+ ':' +
                           str(TR.second))
            debugPrint(0,str(timeReadings))
            for i in range (0, samples):
                mVal = getRawSM(ser)
                readings[i]=mVal;
                debugPrint(5,'sleeping at '+str(timeReadings))
                time.sleep((120.0-5.0)/samples)
                debugPrint(5,'waking at '+str(timeReadings))

            debugPrint(2,str(readings))
            readings.sort()
            debugPrint(2,str(readings))

            outStr=(str(timeReadings) + ' Freq = ' + freq[f] +
                      ' min = ' + getSP(str(readings[0])) +
                      ' median = ' + getSP(str(readings[int(len(readings)/2)])) +
                      ' max = ' + getSP(str(readings[len(readings)-1])))           
            print(outStr)
            print(outStr, file=smf)
            smf.flush()
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

#Open o/p files
smfn = genFileName()
dbfn = smfn.replace('-SM-','-db-')
smf = open(smfn, 'w')

# Configure RX
rxOn(ser)
for f in range (0, len(freq)) :
    setRxParams(ser, freq[f])

ser.flushInput()
debugPrint(0,'Serial port flushed')

TR = datetime.datetime.utcnow()
debugPrint(0,'TR = '+ str(TR))

# Run test
measureNoise(smf)

#All done
#close files and serial port
smf.close()
ser.close()


