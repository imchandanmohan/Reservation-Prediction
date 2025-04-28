pipeline{
    agent any

    stages{
        stage('Cloning Github repo to Jenkins'){
            steps{
                scripts{
                    echo "Cloning Github repo to Jenkins..................."
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github_token', url: 'https://github.com/imchandanmohan/Reservation-Prediction.git']])
                }
            }
        }
    }
} 