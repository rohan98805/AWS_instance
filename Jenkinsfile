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
                    echo "AWS_ACCESS_KEY_ID = $AWS_ACCESS_KEY_ID"
                    echo "AWS_SECRET_ACCESS_KEY length = ${#AWS_SECRET_ACCESS_KEY}"
                    aws --version
                    aws sts get-caller-identity || echo "AWS CLI auth failed"
                    '''
                }
            }
        }
    }
}
