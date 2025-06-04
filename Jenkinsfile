pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        IMAGE_NAME = 'my-app'
        ECR_REPO = '160885287414.dkr.ecr.us-east-1.amazonaws.com/my-app-repo'
    }

    stages {
        stage('Checkout') {
            steps {
                git credentialsId: 'github-credentials', url: 'https://github.com/rohan98805/AWS_instance.git', branch: 'main'
            }
        }

        stage('Login to AWS ECR') {
            steps {
                script {
                    sh 'aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REPO'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Tag and Push to ECR') {
            steps {
                script {
                    sh '''
                        docker tag $IMAGE_NAME:latest $ECR_REPO:latest
                        docker push $ECR_REPO:latest
                    '''
                }
            }
        }

        stage('Clean Up') {
            steps {
                sh 'docker rmi $IMAGE_NAME $ECR_REPO:latest || true'
            }
        }
    }
}
