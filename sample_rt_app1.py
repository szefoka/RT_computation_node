#!/usr/bin/python3

import time

for i in range(100):
    start_time = time.time_ns()

    time.sleep(0.5)

    end_time = time.time_ns()

    print(end_time-start_time)

print("DONE")
