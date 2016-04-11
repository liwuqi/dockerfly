Centos7.1
=====================================

requirements:
----------------

    /opt ext4

* upgrade kernel

```
    rpm -Uvh http://www.elrepo.org/elrepo-release-7.0-2.el7.elrepo.noarch.rpm
    yum install --enablerepo=elrepo-kernel kernel-ml
    yum install --enablerepo=elrepo-kernel kernel-ml-{firmware,headers,devel}
```

* install docker

```
    curl -O -sSL https://get.docker.com/rpm/1.7.1/centos-7/RPMS/x86_64/docker-engine-1.7.1-1.el7.centos.x86_64.rpm
    yum localinstall --nogpgcheck docker-engine-1.7.1-1.el6.x86_64.rpm
```

* config docker


```
    vim /usr/lib/systemd/system/docker.service

    修改:
    ExecStart=/usr/bin/docker -d -H fd:// -s overlay --insecure-registry docker-registry.dev.netis.com.cn:5000 -g /opt/docker

    systemctl docker restart
```

* config dns

```
    vim /etc/hosts
```

add host record

```
    172.16.11.180 docker-registry.dev.netis.com.cn
```

* config double eth route

```
vim /etc/rc.local

ip route add default via 172.16.14.1 dev eno1 table rtem1
ip rule add from 172.16.14.31 table rtem1
ip route add default via 172.16.15.1 dev eno2 table rtem2
ip rule add from 172.16.15.31 table rtem2
ip route flush cache

touch /var/lock/subsys/local
setenforce 0

echo "never" > /sys/kernel/mm/transparent_hugepage/enabled
echo "never" > /sys/kernel/mm/transparent_hugepage/defrag
```

* install nsenter

```
    docker run --rm -v /usr/local/bin:/target docker-registry.dev.netis.com.cn:5000/crossflow/nsenter
```

* install pip
```
    easy_install pip
```


* install dockerfly

```
    mkdir -p /var/www
    cd /var/www/ git clone https://github.com/memoryboxes/dockerfly.git && pip install -r dockerfly/requirements.txt
    cd dockerfly && ./run.sh
```

* set default eth name and default ip address

```
    vim /var/www/dockerfly/dockerflyui/static/js/startup/controller.js
```

change eths config


