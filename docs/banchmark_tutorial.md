
# EDF Benchmarks

We use:
- TODO: [stress-ng](https://manpages.ubuntu.com/manpages/kinetic/en/man1/stress-ng.1.html) for CPU stressing
- Sample python app
- Sample C app

## Benchmark tutorial

Comparing the Sample pthon app performances when it is run on isolated CPU 3 with EDF scheduler and when it's run on the ''non-rt-cpus'' set with the default scheduler.

**First**, please configure the cpusets according the [this](https://github.com/muuurk/RT_computation_node/blob/main/docs/CPU_isolation_n_pEDF.md#tutorial-to-try-out-partitioned-edf-on-your-notebook).

**Run app with EDF:**
```
# cd /sys/fs/cgroup/cpuset/rt_cpus
# echo $$ > tasks

# cd <directory of this git repository>
# chrt -d --sched-runtime 5000000 --sched-deadline 10000000 --sched-period 16666666 0 ./sample_rt_app1.py >> python_app_edf.txt
```
Now the finish times of the app is stored in the ''python_app_edf.txt'' file.

__Open a new terminal and run app with the default scheduler:__
```
./sample_rt_app1.py >> python_app_default_scheduler.txt
```

**Run app with EDF scheduler and background load on the CPU :**
```
# cd /sys/fs/cgroup/cpuset/rt_cpus
# echo $$ > tasks
# stress -c 1
```
In a new terminal:
```
# cd /sys/fs/cgroup/cpuset/rt_cpus
# echo $$ > tasks

# cd <directory of this git repository>
# chrt -d --sched-runtime 5000000 --sched-deadline 10000000 --sched-period 16666666 0 ./sample_rt_app1.py >> python_app_edf_w_cpustress.txt
```

**Run app with the default scheduler and background load on the CPUs :**
```
$ stress -c 3
```
In a new terminal:
```
$ cd <directory of this git repository>
$ ./sample_rt_app1.py >> python_app_default_scheduler_w_cpustress.txt
```
