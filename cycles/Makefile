include ../includes/Makefile.includes

START=5000
END=640000
METHODS=
#METHODS+="local+stateful,cuckoo,hash,rss,CAPA=100000:Stateful 100K" "local+stateful,cuckoo,hash,rss,CAPA=1000000:Stateful 1M"
METHODS+="local+stateful,cuckoo,hash,rss,CAPA=10000000:Stateful 10M"
#METHODS+="local+stateful,cheetah,LB_MODE=rr,CAPA=1000000:Cheetah Stateful 1M"
METHODS+="local+cheetah,stateful,LB_MODE=rr,CAPA=10000000:Cheetah Stateful 10M"
#METHODS+="local+cheetah,serverside,LB_MODE=rr:Cheetah Stateless"
METHODS+="local+cheetah,serverside,obfuscate,LB_MODE=rr:Cheetah Stateless Obfuscated"
#METHODS+="local+cheetah,serverside,hash:Cheetah Stateless Hash"
METHODS+="local+beamer,beamerdecap:Beamer"
METHODS+="local+hash,rss:Hash RSS" "local+hash:Hash DPDK" 

#METHODS="local+cheetah,LB_MODE=rr:Cheetah Stateless LB"
#METHODS="local+hash,rss:Hash RSS"
#METHODS="local+hash:Hash Click"

test:
	${NPF_PATH}/npf-compare.py ${METHODS} --testie ${TESTIE_PATH} --cluster client=nslrack15-100G client=nslrack16-100G client=nslrack17-100G client=nslrack18-100G lb=nslrack14-100G,nic=2+3 server=nslrack20-100G,multi=16,mode=netns server=nslrack21-100G,multi=16,mode=netns server=nslrack19-100G,multi=16,mode=netns server=nslrack22-100G,multi=16,mode=netns --variables VERBOSE=0 PRINT=0 WORKSPACE=${CHEETAH_PATH} --tags stateless --use-last --output --variables "GEN_CONCURRENT=1024" "NSERVER=64" --config n_runs=${N_RUNS} --tags accum rate --show-full  --variables CPU=4 --graph-filename ${EXPE_PATH}/cycles/cyclescompare_req.pdf --variables "GEN_RATE=[${START}*${END}]" FSIZE=8 --config "var_log+={GEN_RATE}" "var_lim+={GEN_RATE:2-680}" --result-path ${EXPE_PATH}/../cyclescompare --config "graph_color={1,1,1,5,5,2,2,2}" "legend_loc=outer lower center" "legend_ncol=3" --graph-size 5 3 --tags parallel --output-columns x all ${NPF_FLAGS}


#"local+stateful,cuckoo,hash,rss,CAPA=10000000:Stateful 10M" "local+cheetah,stateful,CAPA=10000000:Cheetah Stateful 10M" "local+hash,rss:Hash RSS" "local+hash:Hash DPDK"
test_perf:
	${NPF_PATH}/npf-compare.py "local+cheetah:Cheetah Stateless LB" "local+cheetah,serverside:Cheetah Stateless"  --testie ${EXPE_PATH}/../stateful/stateful.testie --cluster client=nslrack15-100G client=nslrack16-100G client=nslrack17-100G client=nslrack18-100G lb=nslrack14-100G,nic=2+3 server=nslrack20-100G,multi=16,mode=netns server=nslrack21-100G,multi=16,mode=netns server=nslrack19-100G,multi=16,mode=netns server=nslrack22-100G,multi=16,mode=netns --variables VERBOSE=0 PRINT=0 WORKSPACE=${CHEETAH_PATH} --tags stateless --use-last --output --variables "GEN_CONCURRENT=1024" "NSERVER=64" --tags rate --show-full  --variables CPU=4 --graph-filename ${EXPE_PATH}/cycles/cyclesperf/ --variables "GEN_RATE=${END}" FSIZE=8 --result-path ${EXPE_PATH}/cycles/.cyclesperf/ --output-columns x all --tags perfclass --variables CPU=2 SCALE=parallel PERF_CLASS_MAP=" ${EXPE_PATH}/cycles/perf.map ../libs/perf/kernel.map" PERF_OPT="--cpu 19" PERF_CLASS_OPT=" --cycles" PERF_MIN=1000000 PERF_FREQ=10000 --config graph_type=barplot --config n_runs=${N_RUNS} ${NPF_FLAGS}

test_obfuscate:
	${NPF_PATH}/npf-compare.py  "local+cheetah,obfuscate,LB_MODE=rr:Load-balancer Obfuscated" "local+cheetah,LB_MODE=rr:Load-balancer" "local+cheetah,serverside,LB_MODE=rr:Server echo" "local+cheetah,serverside,obfuscate,LB_MODE=rr:Server echo Obfuscated"  --testie ${EXPE_PATH}/../stateful/stateful.testie --cluster client=nslrack15-100G client=nslrack16-100G client=nslrack17-100G client=nslrack18-100G lb=nslrack14-100G,nic=2+3 server=nslrack20-100G,multi=16,mode=netns server=nslrack21-100G,multi=16,mode=netns server=nslrack19-100G,multi=16,mode=netns server=nslrack22-100G,multi=16,mode=netns --variables VERBOSE=0 PRINT=0 WORKSPACE=${CHEETAH_PATH} --tags stateless --use-last --output --variables "GEN_CONCURRENT=1024" "NSERVER=64" --config n_runs=${N_RUNS} --tags accum rate --show-full  --variables CPU=4 --graph-filename ${EXPE_PATH}/cycles/cyclesobfuscate/.pdf --variables "GEN_RATE=[${START}*${END}]" FSIZE=8 --config "var_log+={GEN_RATE}" "var_lim+={GEN_RATE:2-680}" --result-path ${EXPE_PATH}/../cyclescompare --variables GEN_RATE=640000 --output-columns x all ${NPF_FLAGS}

test_cpu:
	make test NPF_FLAGS="--variables \"CPU=[1-8]\" GEN_RATE=200000 NSERVER=64 GEN_TIME=15 --tags parallel --config n_runs=3 --tags wrkpath --variables WRK_PATH_FILE=hadoop_size_distribution.path"

plot:
	python3 plot.py









#Internal use only




#Test with stateful lock free hash tables. Considering a backward classification is possible, it makes sense. But the per-core above is simpler to explain and will perform better. If anything we're not faire to Cheetah, so...
test_lf:
	/home/tom/npf/npf-compare.py "local+stateful,cuckoo,hash,rss,lf,CAPA=100000:Stateful LF 100K" "local+stateful,cuckoo,hash,rss,lf,CAPA=1000000:Stateful LF 1M" "local+stateful,cuckoo,hash,rss,lf,CAPA=10000000:Stateful LF 10M" "local+stateful,cheetah,LB_MODE=rr,CAPA=1000000:Cheetah Stateful 1M" "local+cheetah,stateful,LB_MODE=rr,CAPA=10000000:Cheetah Stateful 10M" "local+cheetah,LB_MODE=rr:Cheetah Stateless" "local+hash,rss:Hash RSS" "local+hash:Hash Click" "local+hash:Hash DPDK" --testie /home/tom/workspace/cheetah-experiments/real//../stateful/stateful.testie --cluster client=nslrack15-100G client=nslrack16-100G client=nslrack17-100G client=nslrack18-100G lb=nslrack14-100G,nic=2+3 server=nslrack20-100G,multi=16,mode=netns server=nslrack21-100G,multi=16,mode=netns server=nslrack19-100G,multi=16,mode=netns server=nslrack22-100G,multi=16,mode=netns --variables VERBOSE=0 PRINT=0 WORKSPACE=${CHEETAH_PATH} --tags stateless --use-last --output --variables "GEN_CONCURRENT=1024" "NSERVER=64" --config n_runs=${N_RUNS} --tags rate --show-full --variables CPU=4 --graph-filename /home/tom/workspace/cheetah-experiments/real//cycles/cyclescompare_req.pdf --variables "GEN_RATE=[${START}*${END}]" FSIZE=8 --config "var_log+={GEN_RATE}" "var_lim+={GEN_RATE:2-680}" --result-path /home/tom/workspace/cheetah-experiments/real//../cyclescompare --config "graph_color={1,1,1,5,5,2,2,2}" "legend_loc=outer lower center" "legend_ncol=3" --graph-size 5 3 --output-columns x all
