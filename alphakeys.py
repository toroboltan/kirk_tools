import datetime as datetime
import time

TOTALKEYS = 11

dict_keys = {'KEY0' :'3SAVQIE3TDG93UDE',
             'KEY1' :'GNAWMNJI95O9OXX4',
             'KEY2' :'22WOSKC8IHOY3654',
             'KEY3' :'FTT3MPTRF8E5RXEE',
             'KEY4' :'NBLUSE54O90BPOGK',
             'KEY5' :'HSYA3WWF981D21VP',
             'KEY6' :'J28ZP259ZV8GXUSR',
             'KEY7' :'F0KLT1JC0QOG1SWB',
             'KEY8' :'6QPJ513O2K4GMXN3',
             'KEY9' :'CO86E523NQ3GN7V5',
             'KEY10':'P1CL5XXO5JDJUS4N'}



'''
Are there usage/frequency limits for the API service?

We are pleased to provide free stock API service for our global community 
of users for up to 5 API requests per minute and 500 requests per day. 

If you would like to target a larger API call volume, please visit premium membership.

'''
class alphaKeys():
    
    list_keys = []
    list_timesD = []
    list_timesM = []    
    list_ts = []
    initTs = 0
    callLimDay = 500
    callLimMin = 5
    timelim = 63
    keyInUse = 0
    callExec = 0
    
    def __init__(self):
        print('creating object & loading keys')
        
        self.initTs = datetime.datetime.now().timestamp()
        for i in range(TOTALKEYS):
            keyindex = 'KEY' + str(i)
            self.list_keys.append(dict_keys.get(keyindex))
            self.list_timesD.append(0)
            self.list_timesM.append(0)
            self.list_ts.append(self.initTs)
            
    def PrintKeys(self):
        for i in range(TOTALKEYS):
            print(self.list_keys[i])
            
    def GetAlphaKey(self):
        
        if self.keyInUse == TOTALKEYS:
            self.keyInUse = 0
        
        self.keyInUse
        self.list_keys[self.keyInUse]
        self.list_timesD[self.keyInUse] += 1
        self.list_timesM[self.keyInUse] += 1
        keyVal = self.list_keys[self.keyInUse]
        self.keyInUse += 1
        print(keyVal)
        self.callExec += 1
        if self.callExec == self.callLimMin:
            print('esperando')
            time.sleep(60)
            self.callExec = 0
            print('dale...')
        
        return keyVal

def main():
    mykeys = alphaKeys()
    mykeys.PrintKeys()
    print(mykeys.initTs)
    for i in range(100):
        tmpkey = mykeys.GetAlphaKey()

    for i in range(TOTALKEYS):
        keyVal = mykeys.list_keys[i]
        keyUsg = mykeys.list_timesD[i]
        print('key ' + keyVal + ' has been used  ' + str(keyUsg))
        
if __name__ == '__main__':
    main()
    