# CPU isolation - How to make partitioned EDF on your notebook?

# EDF and its variations for multiple CPU
Earliest deadline first (EDF) or least time to go is **a dynamic priority scheduling algorithm used in real-time operating systems to place processes in a priority queue**. Whenever a scheduling event occurs (task finishes, new task released, etc.) the queue will be searched for the process closest to its deadline.
Source: https://en.wikipedia.org/wiki/Earliest_deadline_first_scheduling

- EDF is designed for a single CPU
- On multiple CPUs, gEDF (Global EDF) and pEDF (Partitioned EDF) are available

# CPUSET
Cpuset is an important concepts in linux system and is created to provide a mechanism to assign a set of cpus and mem nodes to a set of tasks. 

- First of all, **cpuset** is a hierarchical system like a regular file system starting from root directory.
- Each process has a **cpuset** file in procfs which shows where in the hierarchy the process is attached to.

Source: https://codywu2010.wordpress.com/2015/09/27/cpuset-by-example/

**Useful toolset** for configuring cpuset:
https://documentation.suse.com/sle-rt/12-SP5/html/SLE-RT-all/cha-shielding-cpuset.html

Cpusets can bee used to create isolated domains. If you **assign only one CPU to the set** and exectue the task by the EDF scheduler on that cpuset, **you got the partitioned scheduling scheme**.


# FAQs about cpuset

### What is the root cpuset?

The root cpuset, which always exists and always contains all CPUs. It is the ancestor of each user defined cpusets.

### Is it possible to delete CPU from the original root cpuset?

The root cpuset, which always exists and always contains all CPUs, cannot be destroyed.

Source: [https://documentation.suse.com/sle-rt/12-SP5/html/SLE-RT-all/cha-shielding-cpuset.html](https://documentation.suse.com/sle-rt/12-SP5/html/SLE-RT-all/cha-shielding-cpuset.html)

### Can I put every task to a child cpuset?


Yes, e.g., by this command:
```
$ ps -eLo lwp | while read thread; do echo $thread > tasks ; done
```

After this, each new apps that I run were executed by new child cpuset.

### What is cpu_exclusive?

Cpuset.cpu_exclusive flag (0 or 1).  If set (1), the cpuset has exclusive use  of its CPUs (no sibling or cousin cpuset may overlap          CPUs).  By default, this is off (0).  Newly created               cpusets also initially default this to off (0).
Source: https://man7.org/linux/man-pages/man7/cpuset.7.html

### Is it possible to modify the number of cpus in the cpuset while the tasks are executed by that cpuset?

  Yes, I’ve tried and worked :)
 

### How to stress cpus for benchmarks?

[https://linuxhint.com/useful_linux_stress_test_benchmark_cpu_perf/](https://linuxhint.com/useful_linux_stress_test_benchmark_cpu_perf/)

  

### How to start a Deadline process?

  

First set to -1 (TODO: Why?):

[https://access.redhat.com/solutions/1604133](https://access.redhat.com/solutions/1604133)

Second, start the process by defining runtime, deadline and period:

```
$ chrt -d --sched-runtime 5000000 --sched-deadline 10000000 --sched-period 16666666 0 \<command\>
```

## Tutorial to try out partitioned EDF on your notebook

Enter in the cpuset directory and create two cpusets:
```
    # cd /sys/fs/cgroup/cpuset/
    # mkdir cluster
    # mkdir partition
```
Disable load balancing in the root cpuset to create two new root domains in the CPU sets:
```
    # echo 0 > cpuset.sched_load_balance
```
Enter the directory for the cluster cpuset, set the CPUs available to 1-3, the memory node the set should run in (in this case the system is not NUMA, so it is always node zero), and set the cpuset to the exclusive mode.
```
    # cd cluster/
    # echo 1-7 > cpuset.cpus
    # echo 0 > cpuset.mems
    # echo 1 > cpuset.cpu_exclusive 
```
Move all tasks to this CPU set
```
    # ps -eLo lwp | while read thread; do echo $thread > tasks ; done
```
Then it is possible to start deadline tasks in this cpuset.
Configure the partition cpuset:
```
    # cd ../partition/
    # echo 1 > cpuset.cpu_exclusive 
    # echo 0 > cpuset.mems 
    # echo 0 > cpuset.cpus
```
Finally move the shell to the partition cpuset.
```
    # echo $$ > tasks 
```
The final step is to run the deadline workload. E.g., by this command:
```
# chrt -d --sched-runtime 5000000 --sched-deadline 10000000 --sched-period 16666666 0 ./sample_rt_app1.py
```
