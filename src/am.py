import yaml  
import requests
import os,sys
import time 
import datetime 
import threading
import signal


TIMEOUT = 60
configFile = os.path.abspath("conf/am.conf")
dataPath = os.path.abspath("data")  

#if not os.path.exists(dataPath):
#    os.makedirs(dataPath) 
### TO DO 
# 2. 로그 파일이 특정 용량이 되거나 특정 시간이 되면 압축 할 것
class Am():
    name = ""
    url = ""
    interval = 0 
    fsHandle = object() 
    
    def __init__(self, item):
        self.name = item['name']
        self.url = item['url']
        self.interval = item['interval']  
        now = datetime.datetime.now()
        today = now.strftime("%Y-%m-%d")
        fname = self.name+"_"+today+".dat"  
        if not os.path.exists(dataPath):
            os.makedirs(dataPath) 
        fsPath = os.path.join(dataPath, fname)
        fileMode ="a+" 
        self.fsHandle = open(fsPath, fileMode)  
        
    def toRequest(self): 
        while True: 
            now = datetime.datetime.now()
            starttime = time.time() 
            try:
                res = requests.get(self.url,verify=False, timeout=TIMEOUT)
            except ConnectionError as e:
                print(e)
                sys.exit(1) 
                
            if res.status_code < 401:
                endtime = time.time()
                latency = round(endtime-starttime,2)
                self.fsHandle.write("{0}\t{1}\t{2}\n".format(now, self.url, latency)) 
               # print("{0}\t{1}\t{2}\n".format(now, self.url, latency)) 
                self.fsHandle.flush()
            time.sleep(self.interval)
     
def getItem():
    fs = open (configFile, "r")  
    configLoad = yaml.load_all(fs, Loader=yaml.FullLoader) 
    configGen = next(configLoad)  
    return configGen

if __name__ == "__main__":  
    threads = list() 
    Project = list()
    #event = threading.Event() 
    
    item = getItem() 
    # create Thread pool as much as item's length
    for i in item:
        Project.append(Am(i)) 
        
    for k in Project: 
        x = threading.Thread(target=k.toRequest, args=())
        threads.append(x)
        x.start() 
          