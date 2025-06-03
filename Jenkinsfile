pipeline {
    agent any

    environment {
        REMOTE_HOST = 'ec2-user@18.214.129.201'
        REMOTE_KEY = 'ec2-ssh-key' // Jenkins Credential ID
        IMAGE_NAME = 'djangoapp'
        CONTAINER_NAME = 'django_container'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/rohan98805/AWS_instance.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${IMAGE_NAME} .'
            }
        }

        stage('Push to EC2 and Deploy') {
            steps {
                sshagent (credentials: [env.REMOTE_KEY]) {
                    sh """
                    ssh -o StrictHostKeyChecking=no $REMOTE_HOST << 'ENDSSH'
                        docker stop ${CONTAINER_NAME} || true
                        docker rm ${CONTAINER_NAME} || true
                        docker rmi ${IMAGE_NAME} || true
                        cd ~/AWS_instance
                        git pull origin main
                        docker build -t ${IMAGE_NAME} .
                        docker run -d --name ${CONTAINER_NAME} -p 8000:8000 ${IMAGE_NAME}
                    ENDSSH
                    """
                }
            }
        }
    }
}
