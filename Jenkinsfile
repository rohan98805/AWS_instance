pipeline {
    agent any
    environment {
        AWS_DEFAULT_REGION = "us-east-1"
        ECR_REPO = "160885287414.dkr.ecr.us-east-1.amazonaws.com/my-app-repo"
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/rohan98805/AWS_instance.git', branch: 'main'
            }
        }

        stage('Login to AWS ECR') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'aws-credentials',
                                                  usernameVariable: 'AWS_ACCESS_KEY_ID',
                                                  passwordVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    sh '''
                    export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
                    export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
                    AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $ECR_REPO

                    '''
                }
            }
        }


        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t my-app .
                docker tag my-app:latest $ECR_REPO:$IMAGE_TAG
                '''
            }
        }

        stage('Push to ECR') {
            steps {
                sh '''
                docker push $ECR_REPO:$IMAGE_TAG
                '''
            }
        }

        stage('Deploy to EC2') {
            steps {
                sshagent (credentials: ['your-ec2-ssh-key-id']) {
                    sh '''
                    ssh -o StrictHostKeyChecking=no ec2-user@18.214.129.201 << EOF
                    docker pull $ECR_REPO:$IMAGE_TAG
                    docker stop my-app || true
                    docker rm my-app || true
                    docker run -d --name my-app -p 8000:8000 $ECR_REPO:$IMAGE_TAG
                    EOF
                    '''
                }
            }
        }
    }
}
