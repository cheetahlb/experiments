include ../includes/Makefile.includes

PERIOD=10
WAIT=4000
RATE=100

test:
	${NPF_PATH}/npf-compare.py "local+cheetah,LB_MODE=awrr,report,REPORTPERIOD=${PERIOD}:Cheetah - AWRR" "local+cheetah,LB_MODE=pow2,report,REPORTPERIOD=${PERIOD}:Cheetah - Pow2" "local+cheetah,LB_MODE=least,report,REPORTPERIOD=${PERIOD}:Cheetah - Least Loaded" "local+cheetah,LB_MODE=rr:Cheetah - RR" "local+hash,rss:Hash RSS" --testie ${TESTIE_PATH} --cluster ${NPF_CLUSTER} --variables VERBOSE=0 PRINT=0 WORKSPACE=${CHEETAH_PATH} --tags stateless --output --variables "GEN_CONCURRENT=1024" "NSERVER={16,32,64}" --config n_runs=${N_RUNS} --tags rate --variables "SERVER_RATE=${RATE}" --show-full --show-cmd --graph-filename ${EXPE_PATH}/imbalance-bimodal/imbalance_server_bimodal_cpu/.pdf --tags wait --variables "WAIT=${WAIT}" FSIZE=8 --output-columns x all --graph-size 5 3 --config "graph_type={LAT999:boxplot,LAT99:boxplot,PROBELAT99:boxplot,CPUVARS:boxplot}" "var_grid+={CPUVARS}" "graph_show_fliers=0" "legend_loc=outer lower center" "legend_ncol=3" "graph_color={1,2,3,5,2}" "graph_background+={CPUVARS:14}" --tags server_rate bimodal --variables LST_MODE=cpu --result-path ${EXPE_PATH}/imbalance-bimodal/.newbimodal --use-last --config var_log_base+={result-LAT99:2-1000} var_lim+={result-LAT99:0-8000} var_ticks+={result-LAT99:0+500+1000+2000+4000+8000} ${NPF_FLAGS}
