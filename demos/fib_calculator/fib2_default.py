import time
full_start = time.time_ns()

from multiprocessing import Process
from multiprocessing import shared_memory
import os
import mmap
import time

with open("/sys/fs/cgroup/cpuset/rt_cpus/tasks", "a") as f:
    f.write(str(os.getpid()))

f = open("fib2.txt", "w")
f.write("")
f.close()

def shmopen(fn, length):
    f = os.open("/dev/shm/"+fn, os.O_RDWR)
    os.ftruncate(f, length)
    #os.ftruncate(f, 2*1048576)
    mm = mmap.mmap(f, 0, prot=mmap.PROT_WRITE)
    return mm

def fib():
    nterms = 100001
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
fib1 = 0
zero = 0
mmfib.seek(0)
mmtime.seek(0)
#f = os.open("/dev/shm/buffer", os.O_RDWR)
#os.ftruncate(f, 2*1048576)

file_object = open('fib2.txt', 'a')

for i in range(0,10000):
    #while(fib1 == 0):
    #    fib1 = int.from_bytes(mmfib.read(),"little")
    #mmfib.write(zero.to_bytes(1, "little"))
    #mmfib.seek(0)
    #fib1 = int.from_bytes(mmfib.read(),"little")
    #start_time = time.time_ns()
    fib1 = int(mmfib.read().decode("utf-8"))
    #fib1 = int(mmfib.read().decode("utf-8"))
    #print(fib1)
    fib2 = fib()
    start_time = int(mmtime.read().decode("utf-8"))
    end_time = time.time_ns()
    mmfib.seek(0)
    mmtime.seek(0)
    #print(fib1+fib2)
    #print("fib1+fib2 exc. time: {}".format(end_time-start_time))
    #time.sleep(0.23)
    exc_time = time.time_ns()-start_time
    file_object.write("{}\t{}\n".format(start_time, exc_time))
    print("FIB2: {} \t {}".format(start_time, exc_time))
    #os.sched_yield()
    time.sleep(0.23)


file_object.close()

