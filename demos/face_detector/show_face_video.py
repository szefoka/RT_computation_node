import os
import mmap
import numpy as np
import cv2
import sys

def shmopen(fn, length):
    f = os.open("/dev/shm/"+fn, os.O_RDWR)
    os.ftruncate(f, length)
    #os.ftruncate(f, 2*1048576)
    mm = mmap.mmap(f, 0, prot=mmap.PROT_WRITE)
    return mm


mmframe = shmopen("frame", 480*640*3)

while True:

    frame_bytes = mmframe.read()
    frame = np.frombuffer(frame_bytes, dtype='uint8')


    frame = frame.reshape(480,640,3)

    #print(frame)
    cv2.imshow('face detection', frame)

    mmframe.seek(0)
    k = cv2.waitKey(30) & 0xff
    if k==27:
        break

