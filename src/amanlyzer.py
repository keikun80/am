
# file read from data directory
# 첫번째 줄은 시작점
# 측정시간 : 마지막시간 - 첫번째시간
# 측정간격

import os, sys 
import multiprocessing 
from datetime import datetime
import time

dataDir = os.path.abspath("data") 
downInterval = 60
def getFile(Direc = dataDir):
    '''
    get all file in dataDir 
    return : list of data files
    '''   
    retVal = []
    for x in os.listdir(Direc):
        if x.endswith("dat"):
             retVal.append(os.path.abspath(Direc+"/"+x))
    return retVal 
def analyzeFile(f):  
    i = 0
    startDate = 0
    endDate = 0 
    downTime = 0
    prevTime =0
    currentTime = 0 
    print("\n=========================== \n")
    with open (f , "r") as fd: 
        diffTime = dict() 
        for line in fd.readlines():  
            if len(line) <= 1: 
                continue
            item = line.split("\t") 
            if prevTime == 0: 
                prevTimeStr = datetime.strptime(item[0], "%Y-%m-%d %H:%M:%S.%f")  
                prevTime = time.mktime(prevTimeStr.timetuple())  
                startDate = prevTime
                print(f"statistic for {item[1]}")
            elif (prevTime > 0) and (currentTime == 0):
                currentTimeStr = datetime.strptime(item[0], "%Y-%m-%d %H:%M:%S.%f")   
                currentTime = time.mktime(currentTimeStr.timetuple())  
                diffTime[item[0]] = currentTime - prevTime  
                if diffTime[item[0]] >= downInterval: 
                    print(f"down at :{prevTimeStr} ~ {currentTimeStr} : {diffTime[item[0]]} sec")  
                    downTime = downTime + diffTime[item[0]]
                prevTime = currentTime 
                endDate = currentTime
                currentTime = 0 
            else: 
                print("else")
            i = i + 1 
    #print(endDate, startDate, endDate - startDate, downTime)
    print(f"Availabity : {100 - (downTime/(endDate - startDate) * 100)} %") 
if __name__ == "__main__":
    dataFiles = getFile()   
   
    for f in dataFiles:
        analyzeFile(f)