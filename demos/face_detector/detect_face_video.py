try:
    import cv2
except:
    import cv2

import mmap
import os
import sys
import numpy as np
import time

with open("/sys/fs/cgroup/cpuset/rt_cpus/tasks", "a") as f:
    f.write(str(os.getpid()))

def shmopen(fn, length):
    f = os.open("/dev/shm/"+fn, os.O_RDWR, os.O_CREAT)
    os.ftruncate(f, length)
    #os.ftruncate(f, 2*1048576)
    mm = mmap.mmap(f, 0, prot=mmap.PROT_WRITE)
    return mm

mmframe = shmopen("frame", 480*640*3)

# Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# To capture video from webcam.
cap = cv2.VideoCapture(0)
# To use a video file as input
# cap = cv2.VideoCapture('filename.mp4')

print("Recording Webcam...")
print("-------------------------------")
print("FPS\tAVG RUNTIME (in ns) DURING A SEC")
frames_per_sec = 1
pre_sec_time = 0
sum_run_time = 0
while True:

    start_time = time.time_ns()

    if start_time - pre_sec_time > 1000000000:
        avg_run_time = int(sum_run_time/frames_per_sec)
        print("{}\t{}".format(frames_per_sec, avg_run_time))
        pre_sec_time = start_time
        frames_per_sec = 0
        sum_run_time = 0
        frames_per_sec += 1
    else:
        frames_per_sec += 1

    # Read the frame
    _, img = cap.read()

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect the faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Draw the rectangle around each face
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

    #print(type(img))
    #print(img.dtype)
    #print(img.shape)
    mmframe.write(img.tobytes())
    mmframe.seek(0)

    end_time = time.time_ns()

    # Stop if escape key is pressed
    k = cv2.waitKey(30) & 0xff
    if k==27:
        break

    #print(end_time-start_time)
    sum_run_time += end_time-start_time
    os.sched_yield()

# Release the VideoCapture object
cap.release()
