#SM to Spoints

cal=[[0,'S0'],[12,'S1'],[25,'S2'],[41,'S3'],[51,'S4'],[65,'S5'],[80,'S6'],
    [95,'S7'],[112,'S8'],[133,'S9'],[144,'S9+5'],[151,'S9+10'],
    [163,'S9+15'],[172,'S9+20'],[180,'S9+25'],[192,'S9+30'],
    [200,'S9+35'],[213,'S9+40'],[231,'S9+45'],[255,'S9+60'],[256,'junk']]

SMtoSP=[]

debug = False

def SMinit():
    calPtr = 0
    sv = cal[calPtr][1]
    for SMindx in range(256):
        if SMindx == cal[calPtr+1][0]:
           calPtr += 1
           sv = cal[calPtr][1]
        SMtoSP.append(sv)
        
    if debug:
        for SMindx in range(256):
            print(SMindx, ' ', SMtoSP[SMindx])

def getSP(sm):
    return(SMtoSP[int(sm)])
