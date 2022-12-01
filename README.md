# Single node RT FaaS

In the field of Cloud computing, Function as a Service (FaaS) is the latest stage, which makes it possible for users to run their applications in functions without any management effort. On the other hand, if an application (e.g., a robot controller) has real-time execution criteria, developers need to plan in detail the used hardware and its configuration to guarantee the prior defined return time of the application. In this project, we aim to bring these two fields together and enable an RT-FaaS platform, which is able to handle jointly critical and non-critical functions. 

The two significant benefits of such a system are: 
1) there is no need to operate and maintain two different infrastructures (one general-purpose FaaS server and another with special HW tailored for RT executions) 

2) The RT-FaaS takes the burden of performing complex tasks from the developers' shoulders. It allows them to focus only on application development and not care about the server management to enable RT execution

We are aiming to to make an open-source RT-FaaS based on [OpenFaaS](https://www.openfaas.com/), thereby also helping the industries and the research communities to use general purpose hardware for RT and non-RT applications as well, thus ensuring the resiliency and sustainability of the applications and cloud infrastructures.

The structure of this repo is the following:

- demo - Directory of demo applications that can be execute in a RT and non-RT way to illustrate the differences
- docs - Gathered documentation about how to run RT applications
- etc...
