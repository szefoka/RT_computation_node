#!/bin/bash

chrt -d --sched-runtime 220000000 --sched-deadline 450000000 --sched-period 450000000 0 python fib1.py&
PID1=`echo "$!"`
echo $PID1

chrt -d --sched-runtime 220000000 --sched-deadline 450000000 --sched-period 450000000 0 python fib2.py&
PID2=`echo "$!"`
echo $PID2

stress-ng --sequential 0 -t 1s
kill $PID1
sleep 1
kill $PID2

echo "DONE"
