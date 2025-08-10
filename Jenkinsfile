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
                sh 'docker build -t almalinux-ci .'
            }
        }

        stage('Run Container & Execute Scripts') {
            steps {
                sh '''
                docker rm -f almalinux-ci-run || true
                docker run --name almalinux-ci-run -d almalinux-ci sleep infinity

                docker cp install_services.py almalinux-ci-run:/root/install_services.py
                docker exec almalinux-ci-run python3 /root/install_services.py

                docker cp validate_installation.py almalinux-ci-run:/root/validate_installation.py
                docker exec almalinux-ci-run python3 /root/validate_installation.py
                '''
            }
        }
    }

    post {
        always {
            sh 'docker rm -f almalinux-ci-run || true'
        }
    }
}
