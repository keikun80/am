import yaml  
import requests
import os,sys
import time 
import datetime 
import re  
from typing import List, Dict
#sys.path.append(os.path.abspath("lib")) 
from lib import amlog, amconfig

TIMEOUT = 60
#configFile = os.path.abspath("conf/am.conf")
#dataPath = os.path.abspath("data")  
#if not os.path.exists(dataPath):
#    os.makedirs(dataPath) 
### TO DO  
class Am():
    name = ""
    url = ""
    interval = 0 
    fsHandle = object() 
    
    def __init__(self, item: List[Dict[str,str]]) -> None:
        self.name = item['name']
        self.url = item['url']
        self.interval = item['interval']
        self.verify_ssl = item.get('verify_ssl', True)
    
    def logGenerate(self) -> None:
        now = datetime.datetime.now()
        today = now.strftime("%Y-%m-%d")
        fname = self.name+"_"+today+".dat"  
        if not os.path.exists(amconfig.dataDir):
            os.makedirs(amconfig.dataDir) 
        fsPath = os.path.join(amconfig.dataDir, fname)
        fileMode ="a+"
        try: 
            self.fsHandle = open(fsPath, fileMode)
        except Exception as e:
            print(e)
            sys.exit(1)
    def toRequest(self) -> None:
        self.logGenerate() 
        #currentFile = os.path.basename(self.fsHandle.name)  
        #pattern = (r'\d{4}-\d{2}-\d{2}')
        #p = re.compile(pattern) 
        #r = p.search(currentFile).group() 
        while True: 
            currentFile = os.path.basename(self.fsHandle.name)  
            pattern = (r'\d{4}-\d{2}-\d{2}')
            p = re.compile(pattern) 
            r = p.search(currentFile).group()  
            
            now = datetime.datetime.now()
            starttime = time.time() 
            today = now.strftime("%Y-%m-%d") 
            print("r : ", r)
            print("today: ", today) 
            
            if r != today:
                fileName = self.fsHandle.name
                amlog.compress(fileName)
                self.fsHandle.close() 
                self.logGenerate()
                os.unlink(fileName) 
                
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
             
#def getItem() -> List[Dict[str, Any]]:
#    with open(configFile, "r") as confFile:
#        config_load = yaml.load_all(confFile, Loader=yaml.FullLoader)
#        config_gen = next(config_load)
#    return config_gen

if __name__ == "__main__":     
    from multiprocessing import Process
    Project = list() 
    
    item = amconfig.getItem() 
    # create Thread pool as much as item's length
    for i in item:  
        obj = Am(i)
        x = Process(target=obj.toRequest, args=())
        x.start()