pipeline {
    agent any

    environment {
        AWS_REGION = "us-east-1"
        ECR_REPO = "160885287414.dkr.ecr.us-east-1.amazonaws.com/my-app-repo"
        IMAGE_TAG = "latest"
        GIT_REPO = "https://github.com/rohan98805/AWS_instance.git"
        GIT_BRANCH = "main"
        GIT_CREDENTIALS_ID = "github-credentials"  // Make sure this exists in Jenkins Credentials
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: "${GIT_BRANCH}",
                    credentialsId: "${GIT_CREDENTIALS_ID}",
                    url: "${GIT_REPO}"
            }
        }

        stage('Login to AWS ECR') {
            steps {
                sh """
                    aws configure set default.region ${AWS_REGION}
                    aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REPO}
                """
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${ECR_REPO}:${IMAGE_TAG} ."
            }
        }

        stage('Push Docker Image') {
            steps {
                sh "docker push ${ECR_REPO}:${IMAGE_TAG}"
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline completed successfully.'
        }
        failure {
            echo '❌ Pipeline failed. Please check the logs.'
        }
    }
}
