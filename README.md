What is `dockerfly`:
========================

dockerfly is a small Docker tool to help you to create container with independent macvlan Eths simplely.

use dokerfly, you can:

* create a container with one or more macvlan eths by json config file easily,and set independent ip for each veth

* exec command within contianer by nsenter easily

* create a container with sshd service ,then you can visit the container as the same as a normal virtual machine


How to Work:
========================

                                                           +-----------------------------------------------+---------------+
    +---------+                  *******                   |                    Physical hostDocker                        |
    | Physical|                **       **                 |   +---------+           +---------+           +---------+     |
    \ hostA   /              **  Local    **               |   | Docker  |           | Docker  |           | Docker  |     |
    |\       /|  --------->  *   NetWork   *  <----------- |   \ hostA   /           \ hostC   /           \ hostC   /     |
    | ------  |              **           **               |   |\       /|           |\       /|           |\       /|     |
    |         |                **       **                 |   | ------  |           | ------  |           | ------  |     |
    +---------+                  *******                   |   | MacVlan |           | MacVLan |           |...EthC1 |     |
    192.168.1.2                                            |   | EthA    |           | EthB    |           |   EthC2 |     |
                                                           |   +---------+           +---------+           +---------+     |
                                                           |  192.168.1.10           192.168.1.11          192.168.1.12    |
                                                           |                                               192.168.1.13    |
                                                           +-----------------------------------------------+---------------+

```
[PhysicalHostA@localhost]~# ping 192.168.1.10
PING 192.168.159.2 (192.168.1.10) 56(84) bytes of data.
64 bytes from 192.168.1.10: icmp_seq=1 ttl=128 time=0.663 ms
64 bytes from 192.168.1.10: icmp_seq=2 ttl=128 time=0.180 ms
...
```

Install:
========================

* Linux and Docker. I have tested with Docker versions 1.1.0 through 1.3.1, but other versions should work too. Linux kernels after 3.5 are known to work; the newer the better.

* [nsenter](https://github.com/jpetazzo/nsenter):

    ```
    docker run --rm -v /usr/local/bin:/target jpetazzo/nsenter
    ```

*  dockerfly:
    ```
    pip install dockerfly
    ```

How to use:
========================

* generate a sample config json:

    ```
    dockerfly gen centos6.json
    ```

you'll get a sample config, cenos6.json:

    [
        {
            "gateway": "192.168.159.2",
            "eths": [
                [
                    "testDockerflyv0",
                    "eth0",
                    "192.168.159.10/24"
                ],
                [
                    "testDockerflyv1",
                    "eth0",
                    "192.168.159.11/24"
                ]
            ],
            "image_name": "centos:centos6",
            "run_cmd": "/bin/sleep 300"
        }
    ]

this means:

    * you will create a container with two macvlan eths(testDockerflyv0:192.168.159.10/24, testDockerflyv1:192.168.159.11/24), the eths will link to eth0

    * the container's image name is centos:centos6

* start this container:

    ```
     dockerfly.py run centos6.json
    ```
output:

    ```
    Container running:ContainerId(e3974de549891f15e448c4cb0b1b36706b7a233e0d79073a3f4677b3586a4dcb) Pid(28437)
    ```

exec `docker ps`, you can find:

    CONTAINER ID        IMAGE                                    COMMAND             CREATED             STATUS              PORTS               NAMES
    e3974de54989        172.16.11.13:5000/brain/centos6:latest   "/bin/sleep 300"    2 minutes ago       Up 2 minutes                            dockerfly_centos_centos6_20141207121837


* set a simple httpserver by nsenter:

    ```
      nsenter -t 28247 -n python -m SimpleHTTPServer 80
    ```

now you can visit `http://192.168.159.10` in Physical HostA.
