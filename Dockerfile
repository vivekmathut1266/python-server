FROM almalinux:8

ENV container docker

RUN dnf -y update && \
    dnf -y install systemd python3 sudo firewalld && \
    dnf clean all

VOLUME [ "/sys/fs/cgroup" ]
STOPSIGNAL SIGRTMIN+3

CMD ["/usr/sbin/init"]
