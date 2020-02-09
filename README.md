Cheetah experiments
===================

This repository focuses on reproducing experiments, the code of Cheetah itself is available at https://github.com/cheetahlb/cheetah-fastclick. The P4 versions, Kernels, etc are also available at https://github.com/cheetahlb/.
If you're just looking at trying Cheetah, this is not for you. Cheetah repository contains enough simple examples. This repository is made to set up complex, cluster-scale experiments.
This folder contains one sub-folder per experiment. Some figures of Cheetah paper relate to the same experiment. 

Experiments have Makefiles that implement "make test" and sometimes "make plot". Each folder contains a README.md file to describe it.

All tests use NPF to orchestrate experiments. Be sure to set the path to NPF in the folder includes/Makefile.include and all dependencies as described below. While NPF generates graph automatically, we preferred to make fine-tuned graphs using matplotlib ourselves for some of the figure. For some experiments, the data in CSV is provided in this repository, allowing to generate the graphs.

NPF will download and build all dependencies, excluding Cheetah itself.

Testbed
-------
You need 9 machines, 4 for generation, 4 for sink, and 1 for the load balancer itself. You need to define them as per NPF documentation. Use sed to replace reference to nslrack14, the lb, nslrack15 to 20 as clients, nslrack20 to 22 as servers. Clients must be connected to one NIC of the LB, and servers to the other NIC. In practice we used VLANs on an OpenFlow switch, all at 100G.

Prerequisites
-------------

### NPF (https://github.com/tbarbette/npf)
Clone the repository with `git clone https://github.com/tbarbette/npf.git && cd npf`. Install python3 and python3-pip with your system package manager (`sudo apt install python3 python3-pip` for Debian-based systems) and the requirements of NPF with `pip3 install --user -r requirements.txt`. In case of troubles, you may find more help on the [README.md page of NPF](https://github.com/tbarbette/npf#network-performance-framework).

You must define the servers and the NICs to be used *in the cluster folder of NPF*. This is our file for the server:
cluster/server0.node
```
path=/home/tom/npf/
addr=server0.kth.se
//nfs=0

0:ifname=eth0
0:pci=0000:03:00.0
0:mac=50:6b:4b:43:88:ca
```

So you should have 9 of them.

The `path` is the path to NPF on the given machine. It is easer to have NPF in an NFS or other mechanism to share a similar folder between the two machines, under the same path. If you don't have such a setup, uncomment nfs=0 at the top of the file.

The `addr` (address) is the address of the machine.

Then we define 3 variables per NIC: the interface name, the PCIe address, and the MAC address of the NIC. Note that these interfaces are real interfaces, as Cheetah is focusing on dispatching packets in hardware. You may obtain the PCIe address of the interface you want to use with `sudo lshw -c network -businfo`. The NIC informations are used by NPF to automatically replace references in scripts.

The load balancer must have two NICs, just duplicate the 3 last lines.

### Makefiles configuration
As discussed below, all experiments are easily launched using a single Makefile per experiment. As a few parameters depend on your environment (such as the path to the folder where you checked out NPF), we have a single "include" file that resides in the "includes" folder of this repository which is included by all per-experiment Makefiles to set common parameters.
You may define the required variables to in [includes/Makefile.include](includes/Makefile.include). Set `NPF_PATH=path/to/npf` correctly, and change the name of the roles only if you used a different name than "cluster/server0.node" for the NPF cluster configuration files.

### Modified Kernel on the servers
For the experiments involving serverside correction you must have our modified Kernel, available at [https://github.com/cheetahlb/linux](https://github.com/cheetahlb/linux). If you're not familiar with Kernel compilation, instructions are provided in the README.md file of that repository. It is much easier than it is said to be, and faster too if you have a SSD and append `-j8` where 8 is the number of cores on the machine to all `make` commands to build using multiple cores. In a nutshell, those steps should be sufficient for Ubuntu 18.04:
```
MAKEFLAGS=-j8
git clone https://github.com/rsspp/linux.git
cd linux
sudo apt install build-essential libncurses5-dev flex bison openssl libssl-dev libelf-dev libudev-dev libpci-dev libiberty-dev autoconf
cp /boot/config-$(uname -r) .config && make olddefconfig
make bzImage && make modules
sudo make modules install && sudo make install
sudo reboot
```

### Install DPDK on the LB machine
Download DPDK 20.02 at [http://dpdk.org](http://dpdk.org), or directly with `wget http://fast.dpdk.org/rel/dpdk-20.02.tar.xz && tar -Jxvf dpdk-20.02.tar.xz  && cd dpdk-20.02`. Install DPDK's dependencies with `sudo apt install libnuma-dev build-essential python`. To compile DPDK, just use the interactive menu in `./usertools/setup.py`, then choose x86_64-native-linuxapp-gcc, then set up some huge pages, and if you use Intel NICs bind them.

For NPF to be able to build Cheetah automatically (and any DPDK application), you must export the RTE_SDK and RTE_TARGET variables. Edit your .bashrc and add:
```
export RTE_SDK=/home/tom/dpdk
export RTE_TARGET=x86_64-native-linuxapp-gcc
```
Modifying values according to your environment.

### Other dependencies

NPF will download and compile some other dependencies by itself, such as the modified version of WRK2 available at https://github.com/tbarbette/wrk2. The includes folder also contains a few python script that serves various purposes.

Summary of content
------------------

### Experiments
 * cycles is the experiment about cycles per packets
 * dynamic is the PCC experiment
 * imbalance-uniform is the two graphs with the 8K uniform workload
 * imbalance-bimodal is the graph about uniform workload
 * includes contains various configuration and scripts, and the NPF testie files

Understanding the implementation
--------------------------------
Please read the [README.md file of Cheetah's code](https://github.com/cheetahlb/cheetah-click/blob/master/README.md).
 
What if something goes wrong?
-----------------------------
You may append some NPF parameters with the NPF_FLAGS variable such as `make test NPF_FLAGS="--force-retest --show-cmd --show-files --config n_runs=1 --preserve-temporaries"`.
--force-retest will force the test to be done again, even if NPF has some results in cache. --show-cmd will show commands that are launched on the client and server, --show-files will show generated file (such as Click configuration), n_runs=1 configuration parameter reduce the number of runs per tests to 1, while --preserve-temporaries will keep temporary files, scripts, etc so you can launch the test yourself if need be.

One advantage of NPF is the ability to change the defined variables, including from the command line using `--variables CPU=8"` to see what happens with 8 cores.

And of course, do not hesitate to open issues or contact the authors.
