import yaml  
import requests
import os,sys
import time 
import datetime 
from multiprocessing import Process
import re 
sys.path.append(os.path.abspath("lib"))
import log 

TIMEOUT = 60
configFile = os.path.abspath("conf/am.conf")
dataPath = os.path.abspath("data")  
#if not os.path.exists(dataPath):
#    os.makedirs(dataPath) 
### TO DO  
class Am():
    name = ""
    url = ""
    interval = 0 
    fsHandle = object() 
    
    def __init__(self, item): 
        self.name = item['name']
        self.url = item['url']
        self.interval = item['interval']
    
    def logGenerate(self):
        now = datetime.datetime.now()
        today = now.strftime("%Y-%m-%d")
        fname = self.name+"_"+today+".dat"  
        if not os.path.exists(dataPath):
            os.makedirs(dataPath) 
        fsPath = os.path.join(dataPath, fname)
        fileMode ="a+"  
        try: 
            self.fsHandle = open(fsPath, fileMode)
        except Exception as e:
            print(e)
            sys.exit(1)
        
    def toRequest(self):
        self.logGenerate() 
        currentFile = os.path.basename(self.fsHandle.name)  
        pattern = (r'\d{4}-\d{2}-\d{2}')
        p = re.compile(pattern) 
        r = p.search(currentFile).group() 
        while True: 
            now = datetime.datetime.now()
            starttime = time.time() 
            today = now.strftime("%Y-%m-%d") 
            if r != today: 
                log.compress(self.fsHandle.name)
                self.logGenerate()
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
    Project = list() 
    
    item = getItem() 
    # create Thread pool as much as item's length
    for i in item: 
        Project.append(Am(i)) 
    
    for k in Project: 
        x = Process(target=k.toRequest, args=())
        x.start()
