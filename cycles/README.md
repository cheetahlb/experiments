# Cycles experiment
The goal of this serie of experiments is to count the number of cycles each LB methods takes.

Do not forget to set the variables in the includes/Makefile.includes file of the repository. Be sure to have compiled Cheetah and set up NPF correctly.

## Cycles according to the method and request rate
This is the experiment behind the graph of the paper.

make test //Will run the test
make plot //Will generate the paper graph

## Time for server-side cookie fixing and obfuscation
The graph is not published, but the results are referenced in the paper.

make test_obfuscate

Results will be produced as NPF should tell you. Here a are one-liners to get the mean of cycles per methods :

Forward path:
```
fe /home/tom/workspace/cheetah-experiments/real//cycles/cyclesobfuscate/*LB_CYCLESPP.csv 'echo % && cat % | python3 -c "import sys;import numpy as np;print(np.mean(np.array([float(f) for f in sys.stdin.readline().strip().split(\" \")])));"'
/home/tom/workspace/cheetah-experiments/real//cycles/cyclesobfuscate/Load-balancerLB_CYCLESPP.csv
88.069841478
/home/tom/workspace/cheetah-experiments/real//cycles/cyclesobfuscate/Load-balancer_ObfuscatedLB_CYCLESPP.csv
90.0781353916
/home/tom/workspace/cheetah-experiments/real//cycles/cyclesobfuscate/Server_echoLB_CYCLESPP.csv
83.452507173
/home/tom/workspace/cheetah-experiments/real//cycles/cyclesobfuscate/Server_echo_ObfuscatedLB_CYCLESPP.csv
87.1850763433
```
Ie, obfuscation takes 2.06 and 3.73 cycles. Server echo relieves 4,61 cycles

Backward path (obfuscation creates variations):
```
fe /home/tom/workspace/cheetah-experiments/real//cycles/cyclesobfuscate/*LB_CYCLESPP.csv 'echo % && cat % | python3 -c "import sys;import numpy as np;print(np.mean(np.array([float(f) for f in sys.stdin.readline().strip().split(\" \")])));"'
/home/tom/workspace/cheetah-experiments/real//cycles/cyclesobfuscate/Load-balancerLB_CYCLESBWPP.csv
66.4863273643
/home/tom/workspace/cheetah-experiments/real//cycles/cyclesobfuscate/Load-balancer_ObfuscatedLB_CYCLESBWPP.csv
67.3961039787
/home/tom/workspace/cheetah-experiments/real//cycles/cyclesobfuscate/Server_echoLB_CYCLESBWPP.csv
39.837405743
/home/tom/workspace/cheetah-experiments/real//cycles/cyclesobfuscate/Server_echo_ObfuscatedLB_CYCLESBWPP.csv
40.5157387789
```
While here, obfuscation takes 0.91 and 0.68 cycles. Server echo relieves 26.65 cycles.


## Perf test
This test will generate a perf study of the difference between each methods. It uses perf-class.py to map functions to class of functions ot compare performance of lookup vs insertion, etc

make test_perf
