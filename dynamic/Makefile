include ../includes/Makefile.includes

METHODS=
METHODS+="local+beamer:Beamer"
METHODS+="local+cst_hash,rss:Cst Hash"
METHODS+="local+hash,rss:Hash"
#METHODS+="local+cheetah,hash,rss:Cheetah Hash"
METHODS+="local+cheetah,LB_MODE=awrr,report,REPORTPERIOD=10:Cheetah - AWRR"
#METHODS+="local+cheetah,LB_MODE=rr:Cheetah"

N_RUNS=1

test:
	${NPF_PATH}/npf-compare.py ${METHODS} --testie ${TESTIE_PATH} --cluster client=nslrack15-100G client=nslrack16-100G client=nslrack17-100G client=nslrack18-100G lb=nslrack14-100G,nic=2+3 server=nslrack20-100G,multi=16,mode=netns server=nslrack21-100G,multi=16,mode=netns server=nslrack19-100G,multi=16,mode=netns server=nslrack22-100G,multi=16,mode=netns --variables VERBOSE=0 PRINT=0 WORKSPACE=~/workspace/cheetah/ --tags stateless --use-last --output --variables "NSERVER=32" --config n_runs=${N_RUNS} --show-full --show-cmd --show-files --use-last --variables CPU=4 "NETPERNODE=1" --graph-filename ${EXPE_PATH}/dynamic/dynamic/.pdf --tags wait --variables GEN_TIME=40 --output-columns x all --config "graph_y_group={result:median,GNBREQ:median}" --graph-size 5 3 --tags wrkpath campus --variables WRK_PATH_FILE=1024k.path --tags dynamic --variables NSTARTSERVER=24 NSERVERLOAD=24 --config "graph_y_group={GNBREQ:median}" "graph_type={GNBREQ:line}" --tags pygen server_rate --variables GEN_TIME=60 DYNAMIC_START=20 WRK_PATH_FILE=duration_high.path SERVER_RATE=100 GEN_CONCURRENT=12000 --result-path .v2 ${NPF_FLAGS}

plot:
	python3 plot.py
#	python 01-plot-dip-updates.py
#	python 02-plot-dip-updates-drop.py
