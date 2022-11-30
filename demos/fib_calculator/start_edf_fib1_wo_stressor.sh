#!/bin/bash

chrt -d --sched-runtime 220000000 --sched-deadline 450000000 --sched-period 450000000 0 python fib1.py&
PID=`echo "$!"`
echo $PID

sleep 600
kill $PID

echo "DONE"
