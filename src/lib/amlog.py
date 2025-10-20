import gzip,os
import shutil 
import typing  

def compress(logFileName: str) -> None:
    print(logFileName) 
    with open(logFileName,"rb") as f_in:
        with gzip.open(logFileName+".gz", 'wb') as f_out: 
            shutil.copyfileobj(f_in, f_out)
            # I would like to remove when finish zipping 
            
            
if __name__ == "__main__": 
    import datetime, time  
    dataPath = os.path.abspath("data")
    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")
    fname="src/data/thehost_2025-03-10.dat"
    lr = logRotate(fname)
    lr.compress()