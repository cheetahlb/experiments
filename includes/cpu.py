#!/usr/bin/env python3
from time import sleep,time
from parse import parse
from collections import defaultdict
from math import ceil
import argparse
import subprocess

doconn = False
last_idle = defaultdict(int)
last_total = defaultdict(int)
def monitor(id,prefix):
  t = time()
  sleep(ceil(t) - t)
  while True:
    t = time()
    with open('/proc/stat') as f:
      f.readline()
      while True:
        fields = f.readline().strip().split()
        matches = parse("cpu{}", fields[0])
        if matches is None:
            break
        cpuid = int(matches[0])
        if cpuid != id:
            continue
        fields = [float(column) for column in fields[1:]]
        idle, total = fields[3], sum(fields)
        idle_delta, total_delta = idle - last_idle[cpuid], total - last_total[cpuid]
        last_idle[cpuid], last_total[cpuid] = idle, total
        utilisation = 100.0 * (1.0 - idle_delta / total_delta)
        print('CPU-%d-RESULT-%s %f' % (round(t),prefix,utilisation))
        if doconn:
            conns = subprocess.getoutput("netstat -anp | grep :80 | grep ESTABLISHED | wc -l")
            print('CONN-%d-RESULT-%s %s' % (round(t),prefix,conns[-1]))
    try:
        sleep(round(t + 1) - time())
    except KeyboardInterrupt:
        return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Print CPU load.')
    parser.add_argument('cpuid', metavar='N', type=int, nargs=1,
                                help='CPU id')
    parser.add_argument('serverid', metavar='N', type=int, nargs=1,
                                help='Server id')
    args = parser.parse_args()
    monitor(id=args.cpuid[0], prefix='SERVER-%d' % args.serverid[0])
