### Availability monitor 

simple Availability monitor (AM) is based on file of http request result (currently support GET only)

clone this repository
```
git clone https://github.com/keikun80/am.git
```

**am.py** : collect date / url / latency from conf/am.conf file  
It is main script for this AM (should running background process)
```
python am.py &
```
**amanlyzer.py** : analyze down time calcualte on file in data directroy
```
python amanlyzer.py
```

**conf/am.conf** : yaml format config file
You should set name, interval, url   
- *name* is the name of target's and group name of interval and target.
- *interval* is time interval of each requesting.
- *url* is which you will check every request means monitoring availability

```yaml example 
- name: "onehost"
  interval: 10
  url: "https://www.google.com"
- name: "twohost"
  interval: 5
  url: "https://www.naver.com"
- name: "thehost"
  interval: 1
  url: "https://www.python.org"
```
- **data(directroy)** : request result are stored 