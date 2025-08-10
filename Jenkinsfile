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

        stage('Run Installation & Validation') {
            steps {
                sh '''
                # Remove any old container
                docker rm -f almalinux-ci || true

                # Start AlmaLinux container
                docker run --privileged --name almalinux-ci \
                    -v /sys/fs/cgroup:/sys/fs/cgroup:ro \
                    -d almalinux-systemd

                # Copy scripts into container
                docker cp install_services.py almalinux-ci:/root/install_services.py
                docker cp validate_installation.py almalinux-ci:/root/validate_installation.py

                # Run installation
                echo "[INFO] Running installation script..."
                docker exec almalinux-ci python3 /root/install_services.py

                # Run validation
                echo "[INFO] Running validation script..."
                docker exec almalinux-ci python3 /root/validate_installation.py
                '''
            }
        }
    }

    post {
        always {
            sh 'docker rm -f almalinux-ci || true'
        }
    }
}
