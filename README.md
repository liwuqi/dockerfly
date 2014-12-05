简介:
========================
dockerfly采用macvtap作为docker 创建容器时的默认网卡，提供对docker接口的简单wrapper。

使用cokerfly,你可以:

采用简单的配置文件即可以建立一个具有多个独立网卡的container
可以从外部执行container命令


具体请参考:
python2.7 dockerfly.py -h

参考资料:
-------------------------------------

docker:

    https://docs.docker.com/

中文文档:

    http://yeasy.gitbooks.io/docker_practice/content/index.html

网络:

    采用macvtap虚拟网卡，用nsent 添加到container的namespace中，IP从IP池中依次分配

相关工具:

pipework:

    https://github.com/jpetazzo/pipework

nsenter:

    https://github.com/jpetazzo/nsenter
