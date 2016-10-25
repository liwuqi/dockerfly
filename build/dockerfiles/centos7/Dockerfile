# This dockerfile uses the docker-registry.dev.netis.com.cn:5000/brain/centos7 image
# VERSION 1 - EDITION 1
# Author: brain.zhang@netis.com.cn
# Command format: Instruction [arguments / command] ..

# Base image to use, this must be set as the first line
FROM centos:7.1.1503

# Maintainer: docker_user <docker_user at email.com> (@docker_user)
MAINTAINER memorybox memoryboxes@gmail.com

# Commands to add ldap to image
RUN yum clean all  && \
    yum -y swap -- remove fakesystemd -- install systemd systemd-libs && \
    yum -y install openssh-clients openssh-server openssl samba samba-client passwd vim rsyslog wget tar initscripts && \
    ssh-keygen -t rsa -f /etc/ssh/ssh_host_rsa_key -N '' && \
    echo "rootroot" | passwd --stdin root && \
    yum -y install sudo && \
    yum clean all; \
(cd /lib/systemd/system/sysinit.target.wants/; for i in *; do [ $i == systemd-tmpfiles-setup.service ] || rm -f $i; done); \
rm -f /lib/systemd/system/multi-user.target.wants/*;\
rm -f /etc/systemd/system/*.wants/*;\
rm -f /lib/systemd/system/local-fs.target.wants/*; \
rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
rm -f /lib/systemd/system/basic.target.wants/*;\
rm -f /lib/systemd/system/anaconda.target.wants/*;
RUN systemctl enable smb nmb sshd
VOLUME [ "/sys/fs/cgroup" ]

COPY  3rd/dockerservices /etc/dockerservices
COPY  3rd/bin/svscan /usr/bin/
COPY  3rd/bin/supervise /usr/bin/
COPY  3rd/bin/ack /usr/bin/ack
COPY  3rd/bin/startdockerfly.sh /usr/local/bin/startdockerfly.sh

# Commands when creating a new container
CMD ["/usr/local/bin/startdockerfly.sh"]
