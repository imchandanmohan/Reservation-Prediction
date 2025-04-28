pipeline {
    agent any
    environment {
        VENV_DIR = "venv"
    }

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

        stage('Setting up virtual environment and Installing dependencies') {
            steps {
                script {
                    echo 'Setting up virtual environment and Installing dependencies...................'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate

                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }
    }
}
