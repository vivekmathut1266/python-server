pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', 
                    credentialsId: 'github-creds',
                    url: 'https://github.com/vivekmathut1266/python-server.git'
            }
        }

        stage('Build AlmaLinux Image') {
            steps {
                sh 'docker build -t almalinux-systemd .'
            }
        }

        stage('Run Container & Execute Script') {
            steps {
                sh '''
                docker rm -f almalinux-ci || true
                docker run --privileged --name almalinux-ci \
                    -v /sys/fs/cgroup:/sys/fs/cgroup:ro \
                    -d almalinux-systemd

                docker cp install_services.py almalinux-ci:/root/install_services.py
                docker exec almalinux-ci python3 /root/install_services.py
                '''
            }
        }
    }
}
