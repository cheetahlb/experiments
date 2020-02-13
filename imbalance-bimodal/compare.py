import common
import numpy as np
s = common.read_csv("imbalance_server_bimodal_cpu/Cheetah_-_AWRRLAT99.csv")
p = common.read_csv("imbalance_server_bimodal_cpu/Cheetah_-_Pow2LAT99.csv")
c = common.read_csv("imbalance_server_bimodal_cpu/Cheetah_-_RRLAT99.csv")
h = common.read_csv("imbalance_server_bimodal_cpu/Hash_RSSLAT99.csv")
sp = np.nanmean(s[:,1:], axis=1)
cp = np.nanmean(c[:,1:], axis=1)
hp = np.nanmean(h[:,1:], axis=1)
pp = np.nanmean(p[:,1:], axis=1)
print("Awrr vs RR", cp/sp)
print("Awrr vs Hash", hp/sp)
print("Pow2 vs RR", cp/pp)
print("Pow2 vs Hash", hp/pp)
