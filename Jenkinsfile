pipeline {
    agent any

    stages {
        stage('Checkout & Build/Run') {
            steps {
                git branch: 'main',
                    credentialsId: 'github-creds',
                    url: 'https://github.com/vivekmathut1266/python-server.git'

                sh '''
                echo "===== Creating Dockerfile ====="
                cat > Dockerfile <<'EOF'
                FROM almalinux:8
                ENV container docker
                RUN dnf -y update && \
                    dnf -y install systemd python3 sudo firewalld httpd mariadb-server && \
                    dnf clean all
                VOLUME [ "/sys/fs/cgroup" ]
                STOPSIGNAL SIGRTMIN+3
                CMD ["/usr/sbin/init"]
                EOF

                echo "===== Building Docker Image ====="
                docker build -t almalinux-systemd .

                echo "===== Running Container ====="
                docker rm -f almalinux-ci || true
                docker run --privileged --name almalinux-ci \
                    -v /sys/fs/cgroup:/sys/fs/cgroup:ro \
                    -d almalinux-systemd

                echo "===== Copying & Running Script ====="
                docker cp install_services.py almalinux-ci:/root/install_services.py
                docker exec almalinux-ci python3 /root/install_services.py
                '''
            }
        }
    }
}
