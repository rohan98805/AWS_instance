pipeline {
    agent any
    environment {
        AWS_DEFAULT_REGION = 'us-east-1'
    }
    stages {
        stage('Test AWS CLI Authentication') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'aws-credentials',
                                  usernameVariable: 'AWS_ACCESS_KEY_ID',
                                  passwordVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    sh '''
                    export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
                    export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
                    aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 160885287414.dkr.ecr.us-east-1.amazonaws.com/my-app-repo
                    '''
                }

            }
        }
    }
}
