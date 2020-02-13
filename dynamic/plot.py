import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
import matplotlib.ticker as ticker
import os
from matplotlib import container
from common import *
from collections import OrderedDict
import pandas
from matplotlib.markers import MarkerStyle
import sys
import matplotlib

matplotlib.rc('figure', figsize=(4.3, 2.6))


prefix = "dynamic/"
series = []
#series.append(["Stateful_100K", "Stateful_1M", "Cheetah_Stateful_1M" ])
series.extend(["Hash", "Cst_Hash", "Beamer", "Cheetah_-_AWRR" ])
labels = [s.replace("_"," ") for s in series]

labels=["Hash", "Consistent Hash", "Beamer", "Cheetah - AWRR"]

#colors = [shade(c_stateful,0,3), shade(c_stateful,1,3), shade(c_stateful,2,3), shade(c_cheetah_stateful,0,2), shade(c_cheetah_stateful,1,2), shade(c_cheetah,0,1), shade(c_hash,0,3), shade(c_hash,1,3), shade(c_hash,2,3) ]
#colors = [c_stateful, c_beamer, c_cheetah_stateful, c_cheetah, shade(c_hash,0,2), shade(c_hash,1,2) ]

colors = [  shade(c_hash,0,2), shade(c_hash,1,2), c_beamer, c_cheetah  ]

#markers = [ "o", "o", "o", "d", "d", "D", "*", "*", "*" ]
markers = ["*","*","$B$", "d"]

#lines = ["-","-","-","-","-","--","--","--","--","--","--"]
lines = ["--","--",":","-"]


data = []
nbreq = []
nbsrv = []

for i,serie in enumerate(series):
  try:
    f = prefix + serie + "GERR.csv"
    data.append(read_csv(f))
    f = prefix + serie + "GNBREQ.csv"
    nbreq.append(read_csv(f))
    f = prefix + serie + "NBSRV.csv"
    nbsrv.append(read_csv(f))
  except Exception as e:
    del labels[i]
    print("Could not read %s" % serie)
    print(e)
    print("%s:" % f)
    print(open(f, "r").readlines())

for i,serie in enumerate(series):
    x=data[i][:,0]
    #x = x - min(x) - 15
    x = x -15
    y=data[i][:,1:]
    n=nbreq[i][:,1:]
    y = (np.nanmedian(y,axis=1) / np.nanmean(n,axis=1)) * 100

    print(serie,"max -> ",np.max(y))
    mask = [True] * len(x)
    drop = [False] * len(x)


    plt.errorbar(x[mask],y=y[mask],label=labels[i],marker=markers[i],color=colors[i],linestyle=lines[i],markevery=((i + 2) % 5,5))

plt.legend(loc="lower center", bbox_to_anchor=(0.5,1),ncol=2)

ax = plt.gca()
ax2 = ax.twinx()
second_nbreq = False
if second_nbreq:
    for i,serie in enumerate(series):
        x=nbreq[i][:,0]
        #x = x - min(x) - 15
        y=np.nanmedian(nbreq[i][:,1:],axis=1)
        mask = [True] * len(x)
        drop = [False] * len(x)


        plt.errorbar(x[mask],y=y[mask],label=labels[i],marker=markers[i],color=colors[i],linestyle=lines[i],markevery=5)


else:
    for i,serie in enumerate(series):
        if i is not 2:
            continue
#serie=series[0]
        x=nbsrv[i][:,0]
        #x= x-min(x)
        x = x - 15
        s=nbsrv[i][:,1:]

        ax2.plot(x,np.nanmedian(s,axis=1),color="black")
        yp=np.nanmedian(s[x==20])
        ax2.annotate(xy=(20.2,yp+0.2),xytext=(22,yp), s="Number of servers")
    ax2.set_ylim(0,32)

    ax2.set_ylabel("Number of servers")

ax.set_xlabel("Time (s)")
ax.set_ylabel("Broken connections (%)")
ax.set_yscale("symlog", basey=2, linthreshy=1)
ax.set_xlim(0,40)

#ax.set_ylim(50)
ax.set_yticks([0,0.5,1,2,4,8])
ax.grid(axis="y")
def f(x,pos):
    return "%d" % x if x > 1 else "%.1f" % x

ax.yaxis.set_major_formatter(ticker.FuncFormatter(f))

#ax.xaxis.set_minor_formatter(ticker.NullFormatter())
#ax.xaxis.set_major_formatter(ticker.FuncFormatter(f))

#"cyclescompare_req/Hash_DPDKLB_CYCLESPP.csv"


plt.tight_layout()

plt.savefig('new_dip_updates.pdf')
