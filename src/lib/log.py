
## log rotate
## log reopen
import gzip,os
import shutil 

class logRotate:
    def __init__(self, filename):   
        self.logFileName = filename 
   
    def compress(self):
        print(self.logFileName) 
        with open(self.logFileName,"rb") as f_in:
            with gzip.open(self.logFileName+".gz", 'wb') as f_out: 
                shutil.copyfileobj(f_in, f_out)


def compress(logFileName):
    print(logFileName) 
    with open(logFileName,"rb") as f_in:
        with gzip.open(logFileName+".gz", 'wb') as f_out: 
            shutil.copyfileobj(f_in, f_out) 
            
            
if __name__ == "__main__": 
    import datetime, time  
    dataPath = os.path.abspath("data")
    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")
    fname="src/data/thehost_2025-03-10.dat"
    lr = logRotate(fname)
    lr.compress()