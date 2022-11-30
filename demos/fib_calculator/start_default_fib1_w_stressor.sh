#!/bin/bash

python fib1_default.py&
PID=`echo "$!"`
echo $PID

stress-ng --sequential 0 -t 1s
sleep 3
kill $PID

echo "DONE"
