pipeline {
    agent any

    environment {
        AWS_REGION = "us-east-1"
        ECR_REPO = "160885287414.dkr.ecr.us-east-1.amazonaws.com/my-app-repo"
        IMAGE_TAG = "latest"
        GIT_REPO = "https://github.com/rohan98805/AWS_instance.git"
        GIT_BRANCH = "main"
        GIT_CREDENTIALS_ID = "github-credentials"
        AWS_CREDENTIALS_ID = "aws-credentials"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: env.GIT_BRANCH,
                    credentialsId: env.GIT_CREDENTIALS_ID,
                    url: env.GIT_REPO
            }
        }

        stage('Login to AWS ECR') {
            steps {
                withCredentials([usernamePassword(credentialsId: env.AWS_CREDENTIALS_ID, usernameVariable: 'AWS_ACCESS_KEY_ID', passwordVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    sh '''
                    aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
                    aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
                    aws configure set default.region ${AWS_REGION}

                    aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REPO}
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                docker build -t ${ECR_REPO}:${IMAGE_TAG} .
                """
            }
        }

        stage('Push Docker Image') {
            steps {
                sh """
                docker push ${ECR_REPO}:${IMAGE_TAG}
                """
            }
        }

        // Optional: Add a stage to deploy the container to EC2 via SSH or other means

    }

    post {
        success {
            echo 'Pipeline completed successfully.'
        }
        failure {
            echo 'Pipeline failed. Please check the logs.'
        }
    }
}
