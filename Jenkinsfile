pipeline {
    agent any

    environment {
        REMOTE_HOST = 'ec2-user@18.214.129.201'
        REMOTE_KEY = 'ec2-ssh-key' // Jenkins SSH Credentials ID
        REPO_NAME = 'AWS_instance'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/rohan98805/AWS_instance.git'
            }
        }

        stage('Deploy to EC2 with Docker Compose') {
            steps {
                sshagent (credentials: [env.REMOTE_KEY]) {
                    sh """
                    ssh -o StrictHostKeyChecking=no $REMOTE_HOST << 'ENDSSH'
                        cd ~/${REPO_NAME}
                        git pull origin main

                        docker-compose down || true
                        docker-compose build
                        docker-compose up -d
                    ENDSSH
                    """
                }
            }
        }
    }

    post {
        success {
            echo "✅ Deployment complete!"
        }
        failure {
            echo "❌ Deployment failed!"
        }
    }
}
