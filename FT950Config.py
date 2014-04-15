#Setup parameters for FT950
import serial
import time
import FT950SMtoSP

debug0 = True
debug1 = True #Preamp 2!!!! UNCAL!!!
debug2 = False #report smeter value

def debugPrint(level,debugStr):
    if ((level==0 and debug0) or
        (level==1 and debug1) or
        (level==2 and debug2)):
        print('Debug',level,'-',debugStr)
    
def setParam(ser, uStr):
    bStr=bytes(uStr,'utf-8')
    ser.write(bStr)
    time.sleep(0.1)

def rxOn(ser):
    debugPrint(0,'Turning On Rx')
    bStr=bytes('PS1;','utf-8')
    ser.write(bStr) #Turn FT950 on if it is off
    time.sleep(0.1)
    ser.write(bStr) #Turn FT950 on if it is off
    time.sleep(3)
    debugPrint(0,'Rx now on')
    FT950SMtoSP.SMinit()
    

def setRxParams(ser, f):
    debugPrint(0,'Initializing '+f)
    setFreq(ser, f) 
    setParam(ser,'FR0;') #RX VFO A
    setParam(ser,'MD03;') #Mode = CW
    setParam(ser,'NA01;') #Narrow
    setParam(ser,'SH007;') #bandwidth = 500Hz
    setParam(ser,'AG0000;') #AF Gain = 0
    setParam(ser,'AN01;') #Ant 1
    setParam(ser,'BC00;') #Auto Notch off
    setParam(ser,'BP00000;') #Manula Notch off
    setParam(ser,'CO0000;') #Contour off
    setParam(ser,'NB00;') #Noise blanker off
    setParam(ser,'NR00;') #Noise reduction off
    setParam(ser,'PA01;') #Amp1 selected
    if debug1:
        setParam(ser,'PA02;') #Amp2 selected
    setParam(ser,'RA00;') #Attenuator off
    setParam(ser,'RF00;') #Roofing filter Auto
    setParam(ser,'RG0255;') #RF Gain at Max (check this is correct)
    setParam(ser,'RT0;') #clarifier off
    setParam(ser,'SQ0000;') #Squelch zero
    #Do we need to set any EX functions
    #What AGC setting do we need
    #Do we need to worry about IF shift
    #What is the VRF Filter?
    debugPrint(0,'Initializing complete '+f)

def setFreq(ser, f):
    debugPrint(0,'Setting Frequency to ' + str(f))
    setParam(ser,'FA'+ f +';')

def getRawSM(ser):
    ser.write(b'SM0;') #get S-Meter
    mStr = bytes(ser.read(size=7))
    mVal = ((int(mStr[3])-ord('0'))*100 +
           (int(mStr[4])-ord('0'))*10 +
            int(mStr[5])-ord('0'))
    debugPrint(2,'mStr='+str(mStr)+str(' mval=')+str(mVal))
    return(mVal)

def getSP(sm):
    return(FT950SMtoSP.getSP(sm))
