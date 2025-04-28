pipeline {
    agent any

    stages {
        stage('Cloning Github repo to Jenkins') {
            steps {
                script {
                    echo 'Cloning Github repo to Jenkins...................'
                    checkout([$class: 'GitSCM',
                        branches: [[name: '*/main']],
                        userRemoteConfigs: [[
                            credentialsId: 'github_token',
                            url: 'https://github.com/imchandanmohan/Reservation-Prediction.git'
                        ]]
                    ])
                }
            }
        }
    }
}
