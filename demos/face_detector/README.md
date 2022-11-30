
# Face Detector Demo using a normal notebook

This is a face detector demo where we demonstrate the difference between a **best-effort process execution** (scheduled by default CFS of Ubuntu) and the **real-time**, i.e., (near-)deterministic execution of the same task.

We use a face detector application which consist of two components: a *Detector* and a *Projector* element. 

**Detector**:
 - we examine this component to run in the best-effort and the real-time way
 - this periodic task uses your webcam to get a video frame
 - it runs the face detector model on the image
 - it writes the video frame with the detected faces into the memory (/dev/shm/frame)


**Projector**:
 - this is the helper component to make the demo spectacular
 - this reads the shared memory (/dev/shm/frame) to get the newest video frame with the detected 
 - it shows the video frame on your screen

## Tutorial for running the demo

### Configure CPUSETs to enable EDF on your notebook

We are going to use two cpu sets: one set including one CPU for testing the real-time execution and another one to run all of your other stuff on your computer.

Follow the instructions behind the link to configure your cpusets:
https://github.com/muuurk/RT_computation_node/blob/main/docs/CPU_isolation_n_pEDF.md#tutorial-on-how-to-make-partitioned-edf-on-your-notebook

### Init and run the Projector component
This will show the webcam images coming from the Detector component.
```
# touch /dev/shm/frame
# python3 show_face_video.py 
```
### Step 1: Test the application with best effort execution

First, run the Detector component:
```
# python3 detect_face_video.py
```
If everything went well, you are gonna see an output like this:
```
Recording Webcam...
-------------------------------
FPS	AVG RUNTIME (in ns) DURING A SEC
1	0
7	153744848
9	117912454
9	121020615
8	126280415
9	122270114
9	121852476
9	125309273
```
Second, run the Projector component:
```
# python3 show_face_video.py 
```
If everything went well you're going to see the video stream of your webcame with the detected faces on it.

This is the optimal environment for the best-effort execution, since there is no other background processes on the same cpuset where our Detector component runs. Now let's see what happens if we got multiple other tasks running in the background. Let's examine how this influence the Detector's FPS and running time.

Open a new console and run the stressor application:
```
# cd /sys/fs/cgroup/cpuset/rt_cpus/
# echo $$ > tasks
# stress-ng --sequential 0 -t 2s
```
While the stressors are running, I got the folllowing output of the Detector on my notebook:
```
Recording Webcam...
-------------------------------
FPS	AVG RUNTIME (in ns) DURING A SEC
1	0
6	172025515
9	123726848
8	126979915
8	128611273
8	125432850
8	127829538
5	210664202		<--- this is when I turned on the stressor
4	334766076
2	607441017
3	821562383
2	670491889
2	535104813
1	1253961960
2	935470015
2	490864567
```

### Step 2: Test the application with real-time execution

In this scenario, we are going to use the EDF scheduler to guarantee the near-deterministic response time of the Detector.

First, let's calculate the necessary parameters to running your RT application. Give 1 sec CPU time in each 2 sec (in this case the demanded *runtime* is 1 sec and the i*nvocation period* (which is also the *deadline* in our case) is 2 sec) and see what happens:
```
# chrt -d --sched-runtime 1000000000 --sched-deadline 2000000000 --sched-period 2000000000 0 python3 detect_face_video.py 
Recording Webcam...
-------------------------------
FPS	AVG RUNTIME (in ns) DURING A SEC
1	0
1	387692514
1	124335478
1	115075817
1	118502958
1	119859118
1	115899280
1	111722777
1	124683632
1	125242390
```
Here we see, the runtime of an invocation of the Detector is around ~120 ms. So (just to make sure) I'm gonna use the following parameters:
 - runtime = 140 ms
 - period = 160 ms
 - deadline = 160 ms

Run the RT Detector:
```
# chrt -d --sched-runtime 140000000 --sched-deadline 160000000 --sched-period 160000000 0 python3 detect_face_video.py 
Recording Webcam...
-------------------------------
FPS	AVG RUNTIME (in ns) DURING A SEC
1	0
4	216314956
6	145559671
6	154966062
6	159947325
6	159932664
6	158810696
6	158511874
6	160759043
```

To sum up, the RT Detector components perform a detection cycle on a webcam image within ~160 ms, if we don't have other tasks, i.e., stressors, running in the background using the same CPU. Let's examine the stressed case!

Start the stressor:
```
# cd /sys/fs/cgroup/cpuset/rt_cpus/
# echo $$ > tasks
# stress-ng --sequential 0 -t 2s
```
While the stressors are running, I got the folllowing output of the Detector on my notebook:
```
# chrt -d --sched-runtime 140000000 --sched-deadline 160000000 --sched-period 160000000 0 python3 detect_face_video.py 
Recording Webcam...
-------------------------------
FPS	AVG RUNTIME (in ns) DURING A SEC
1	0
5	166748548
6	158701677
6	154680705
6	151182532
6	149006050
6	149432423
6	150666128    <--- this is when I turned on the stressor
6	148100377
6	147626835
6	149000639
6	151609430
6	150385670
6	151890570
6	152719654
```
 We can see here that the execution of the RT Detector is guaranteed and the background stressor tasks cannot influence it's performance.



Sima szerveren:

Webcam helyett egy kép!

CFS MEGOLDÁS:

Indítani a face detectort:
root@c220g1:/users/szefoka/RT_computation_node/demos/facedetection-master# python detect_face_video.py

Közben stressor-ok:
root@c220g1:~# stress-ng --sequential 0 -t 1s

Kimenet:
149773761
140100458
144638489
142056157
141308626
138017996
489118496
7
1134856434
1
1275572781
1
524895114
1420784118
2
138535958
138840216
137969659
138835919
138118094
138743236
138318385
138742489
8
138078931
138763669
138300235
138879354
138192914
138824196
138058178
138825370

fps függ az arcok számától, a kép nagyságátál, stb.

EDF MEGOLDÁS:

- láttuk, hogy alapból ~138 ms alatt végez egy ciklussal

Indítsuk EDF-fel a következőképp:
root@c220g1:/users/szefoka/RT_computation_node/demos/facedetection-master# chrt -d --sched-runtime 141000000 --sched-deadline 142000000 --sched-period 142000000 0 python detect_face_video.py

Felfedezés: Ha túl szigorú a runtime, akkor rosszabb lesz.

-----------------------------------------------------------------------------------------------------------------------
SAJÁT LAPTOP |
--------------

