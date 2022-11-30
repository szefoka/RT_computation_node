#!/bin/bash

python fib1_default.py&
PID=`echo "$!"`
echo $PID

sleep 600
kill $PID

echo "DONE"
