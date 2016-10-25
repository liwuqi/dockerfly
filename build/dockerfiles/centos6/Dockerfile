# This dockerfile uses the docker-registry.dev.netis.com.cn:5000/brain/centos6 image
# VERSION 1 - EDITION 1
# Author: brain.zhang@netis.com.cn
# Command format: Instruction [arguments / command] ..

# Base image to use, this must be set as the first line
FROM centos:6.6

# Maintainer: docker_user <docker_user at email.com> (@docker_user)
MAINTAINER memorybox memoryboxes@gmail.com

# Commands to add ldap to image
RUN yum clean all  && \
    yum -y install openssh-clients openssh-server samba samba-client samba-common vim rsyslog wget tar && \
    ssh-keygen -t rsa -f /etc/ssh/ssh_host_rsa_key -N '' && \
    echo "rootroot" | passwd --stdin root && \
    yum -y install sudo && \
    yum clean all && \
    rm -rf /etc/localtime && \
    /bin/ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    /bin/sed -i "s/UTC/Asia\/Shanghai/g" /etc/sysconfig/clock && \
    echo "alias tail='tail ---disable-inotify'">>/root/.bashrc

COPY  3rd/dockerservices /etc/dockerservices
COPY  3rd/bin/svscan /usr/bin/
COPY  3rd/bin/supervise /usr/bin/
COPY  3rd/bin/ack /usr/bin/ack
COPY  3rd/bin/startdockerfly.sh /usr/local/bin/startdockerly.sh
COPY  3rd/etc/smb.conf /etc/samba/
COPY  3rd/etc/grub.conf /boot/grub/grub.conf

# Commands when creating a new container
CMD ["/usr/local/bin/startdockerfly.sh"]
