import subprocess
import re
import threading
from queue import Queue

def getinfo(ip,q):
    obj = subprocess.getoutput('ping -n 5 '+ip)
    # ptn2 = r"\d+% [\u4E00-\u9FA5]+"
    # gg = re.findall(ptn2,obj)
    ptn = re.compile(r"[\u4E00-\u9FA5]+ = \d+ms")
    ptn2 = re.compile(r"\d+% [\u4E00-\u9FA5]+")
    gg1 = ptn.findall(obj)
    gg2 = ptn2.findall(obj)
    gg1.extend(gg2)
    gg1.append(ip)
    q.put(gg1)

if __name__ == '__main__':
    threads = []
    q = Queue()
    with open('dnslist','r') as dl:
        dnslist = dl.readlines()
    for i in dnslist:
        thread = threading.Thread(target=getinfo,args=(i.strip(),q))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    result = []
    for _ in threads:
        result.append(q.get())
    for res in result:
        print(res)