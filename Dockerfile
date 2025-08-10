FROM almalinux:8

ENV container docker

# Install required packages only
RUN dnf -y update && \
    dnf -y install systemd python3 sudo firewalld procps-ng net-tools && \
    dnf clean all

# Enable cgroup mount for systemd
VOLUME [ "/sys/fs/cgroup" ]
STOPSIGNAL SIGRTMIN+3

CMD ["/usr/sbin/init"]
