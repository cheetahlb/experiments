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
import argparse

parser = argparse.ArgumentParser(description='Grapher for the cycles experiment.')

parser.add_argument("--presentation", default=False, action='store_true')


args = parser.parse_args()


if args.presentation:
    extension = 'svg'
    matplotlib.rc('figure', figsize=(6.5, 3.1))
else:
    extension = 'pdf'
    matplotlib.rc('figure', figsize=(5.1, 3.1))


show_slow = False

prefix = "cyclescompare_req/"
#series.append(["Stateful_100K", "Stateful_1M", "Cheetah_Stateful_1M" ])

c_stateful = graphcolor[0]
c_cheetah = graphcolor[8]

#c_cheetah_stateful = graphcolor[4]
c_cheetah_stateful = shade(c_cheetah,1,2)
c_cheeath = shade(c_cheetah,0,2)
c_hash = graphcolor[2]
c_beamer = graphcolor[6]
#colors = [shade(c_stateful,0,3), shade(c_stateful,1,3), shade(c_stateful,2,3), shade(c_cheetah_stateful,0,2), shade(c_cheetah_stateful,1,2), shade(c_cheetah,0,1), shade(c_hash,0,3), shade(c_hash,1,3), shade(c_hash,2,3) ]

#markers = [ "o", "o", "o", "d", "d", "D", "*", "*", "*" ]
#markers = ["o", "$B$", "d","*", "D","*"]

#lines = ["-","-","-","-","-","--","--","--","--","--","--"]
#lines = ["-","--","-","--","--","--","--"]


#  colors = [c_stateful, c_beamer, c_cheetah_stateful, shade(c_hash,0,2), c_cheetah, shade(c_hash,1,2) ]

suffixes = np.arange(5) + 1

for suffix in suffixes:
    plt.clf()
    series = []
    labels = []
    colors = []
    lines = []
    markers = []

    do_beamer = False
    do_cheetah_stateful = False
    do_hash = False
    do_cheetah = False
    if suffix > 3:
        do_beamer = True
    if suffix > 2:
        do_hash = True
    if suffix > 1:
        do_cheetah = True
    if suffix > 4:
        do_cheetah_stateful = True

    series.extend(["Stateful_10M"])
    labels.extend(["Stateful Cuckoo"])
    colors.append(c_stateful)
    lines.append("-")
    markers.append("o")

    if do_beamer:
        series.extend(["Beamer"])
        labels.extend(["Beamer"])
        colors.append(c_beamer)
        lines.append("--")
        markers.append("$B$")
    if do_cheetah_stateful:
        series.extend(["Cheetah_Stateful_10M"])
        labels.extend(["Stateful Cheetah"])
        colors.append(c_cheetah_stateful)
        lines.append("-")
        markers.append("d")
    if do_hash:
        series.extend(["Hash_DPDK"])
        labels.extend(["Hash (SW)"])
        colors.append(shade(c_hash,0,2))
        lines.append("--")
        markers.append("*")
    if do_cheetah:
        series.extend(["Cheetah_Stateless"])
        labels.extend(["Stateless Cheetah"])
        colors.append(c_cheetah)
        lines.append("--")
        markers.append("D")
    if do_hash:
        series.extend(["Hash_RSS" ])
        labels.extend(["Hash (HW)"])
        colors.append(shade(c_hash,1,2))
        lines.append("--")
        markers.append("*")
#labels = [s.replace("_"," ") for s in series]
#labels = ["Stateful Cuckoo","Beamer", "Stateful Cheetah", "Hash (SW)",  "Stateless Cheetah", "Hash (HW)"]
#labels[-2] = "Hash (SW)"
#labels[-1] = "Hash (HW)"

    data = []
    nbreq = []
    cols=range(10)
#cols=range(3)
#cols=None
    for i,serie in enumerate(series):
      try:
        f = prefix + serie + "LB_CYCLESPP.csv"
        data.append(read_csv(f))
        f = prefix + serie + "REQUEST.csv"
        nbreq.append(read_csv(f))
      except Exception as e:
        del labels[i]
        print("Could not read %s" % serie)
        print(e)
        print("%s:" % f)
        print(open(f, "r").readlines())

    for i,serie in enumerate(series):
        x=data[i][:,0]
        r=x>=5000
        x=x[r]
        y=data[i][:,1:][r]

        req=[]
        for v in x:
            for r in nbreq[i]:
                if v == r[0]:
                    req.append(np.nanmean(r[1]) * 1445)
        req = np.asarray(req)
        #diff = np.nanmedian(y,axis=1) / np.nanmedian(data[4][:,1:],axis=1)
        #print(serie,diff,np.max(diff) )
        if show_slow:
            mask = (x - req) < (0.01 * req)
            drop = (x - req) >= (0.01 * req)
        else:
            mask = [True] * len(x)
            drop = [False] * len(x)
        drop = [ (drop[i] or (mask[i - 1] if i > 0 else False)) for i in range(len(drop)) ]

        mean = True
        if mean:
            yv = np.nanmean(y,axis=1)
            errn = np.nanstd(y,axis=1)
            errp = np.nanstd(y,axis=1)
        else:
            yv = np.nanmedian(y,axis=1)
            errn = np.nanpercentile(y,75,axis=1) - yv
            errp = yv - np.nanpercentile(y,25,axis=1)

        plt.errorbar(x[mask],y=yv[mask],yerr=(errp[mask],errn[mask]),label=labels[i],marker=markers[i],color=colors[i],linestyle=lines[i])
        plt.errorbar(x[drop],y=yv[drop],yerr=(errp[drop],errn[drop]),label=None, fillstyle="none",marker=markers[i],linestyle=':',color=colors[i])

    plt.legend(loc="lower center", bbox_to_anchor=(0.45,1),ncol=3 if len(labels) > 4 else 2, prop={'size': 8.5} )

    ax = plt.gca()
    ax.set_xscale("symlog")
    ax.set_xticks(x)
    ax.set_ylim(50,450)
    ax.set_xlabel("Requests per seconds")
    ax.set_ylabel("Cycles / packets")
    ax.set_yscale("symlog")

#ax.set_ylim(50)
    ax.set_yticks([50,100,200,400])
    ax.grid(axis="y")
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter("%d"))
    def f(x,pos):
        return "%dK" % (x / 1000)

    ax.xaxis.set_minor_formatter(ticker.NullFormatter())
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(f))

#"cyclescompare_req/Hash_DPDKLB_CYCLESPP.csv"


    plt.tight_layout()

    plt.savefig('cycles%d.%s' % (suffix,extension),  bbox_inches='tight' )
