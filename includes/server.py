import requests
import threading
import time
import sys
import psutil
import argparse
import re

parser = argparse.ArgumentParser(description='Load reporter')
class StoreDictKeyPair(argparse.Action):
     def __call__(self, parser, namespace, values, option_string=None):
         my_dict = {}
         for kv in re.split(",| ",values.strip()):
             k,v = re.split("=|:",kv)
             my_dict[k] = v
         setattr(namespace, self.dest, my_dict)

parser.add_argument("--servers", dest="servers", action=StoreDictKeyPair, metavar="SERVERID=CPUID,SERVERID=CPUID...")
parser.add_argument("--lb", dest="lb", type=str)
parser.add_argument("--interval", dest="interval", type=int, default=1000)
args = parser.parse_args(sys.argv[1:])


url = "http://" + args.lb + "/cheetah/load"
print("URL is %s" % url)
while 1:
    time.sleep(float(args.interval) / 1000.0)
    #load = int(psutil.cpu_percent())
    cpu = psutil.cpu_percent(percpu=True)
    data = []
    for serverid,cpuid in args.servers.items():
        load = int(cpu[int(cpuid)])
        data.append(str(serverid)+':'+str(load))
    try:
        r = requests.post(url, data = ','.join(data))
    except Exception as e:
        #print("Could not connect")
        #print(e)
        continue


