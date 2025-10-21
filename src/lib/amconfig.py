from typing import List, Dict, Any 
import yaml 
import os 


configFile = os.path.abspath("conf/am.conf")  
dataDir = os.path.abspath("data") 

def getItem() -> List[Dict[str, Any]]: 
    with open(configFile, "r") as confFile:
        config_load = yaml.load_all(confFile, Loader=yaml.FullLoader)
        config_gen = next(config_load)
    return config_gen

if __name__ == "__main__":
    print(getItem())