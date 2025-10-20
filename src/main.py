import amanlyzer 
import amcollector
import time 


if __name__ == "__main__":    
    from multiprocessing import Process
    Project = list() 
    
    item = amcollector.getItem() 
    # create Thread pool as much as item's length
    for i in item:  
        obj = amcollector.Am(i)
        x = Process(target=obj.toRequest, args=())
        x.start() 
        x.join()