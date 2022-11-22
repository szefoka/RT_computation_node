from multiprocessing import Process
from multiprocessing import shared_memory
import os
import mmap
import time

with open("/sys/fs/cgroup/cpuset/partition/tasks", "a") as f:
    f.write(str(os.getpid()))

def shmopen(fn, length):
    f = os.open("/dev/shm/"+fn, os.O_RDWR, os.O_CREAT)
    os.ftruncate(f, length)
    #os.ftruncate(f, 2*1048576)
    mm = mmap.mmap(f, 0, prot=mmap.PROT_WRITE)
    return mm

def fib():
    nterms = 100000
    n1, n2 = 0, 1
    count = 0
    while count < nterms:
        nth = n1 + n2
        n1 = n2
        n2 = nth
        count += 1
    #print(nth)
    return nth

mmfib = shmopen("fib", 20899) 
mmtime = shmopen("time", 19)
for i in range(0,100):
    start_time = time.time_ns()
    #mmfib.write(fib().to_bytes(1048576, "little"))
    mmfib.write(bytes(str(fib()),'utf-8'))
    mmtime.write(bytes(str(start_time), 'utf-8'))
    #mmtime.write(start_time.to_bytes(1048576, "little"))
    mmfib.seek(0)
    mmtime.seek(0)
    print(time.time_ns()-start_time)
