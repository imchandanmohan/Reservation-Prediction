pipeline {
    agent any
    environment {
        VENV_DIR = "/var/jenkins_home/workspace/venv"
        PYTHON = "/usr/bin/python3"
    }

    stages {
        stage('Debug Info') {
            steps {
                sh '''
                    echo "=== Debug Information ==="
                    echo "Workspace path: ${WORKSPACE}"
                    echo "Python path: ${PYTHON}"
                    echo "Python version:"
                    ${PYTHON} --version
                    echo "Workspace permissions:"
                    ls -ld ${WORKSPACE}
                    echo "Current user:"
                    whoami
                    echo "=== Environment ==="
                    env
                '''
            }
        }

        stage('Create Virtual Environment') {
            steps {
                sh '''
                    echo "Creating virtual environment at ${VENV_DIR}"
                    ${PYTHON} -m venv ${VENV_DIR} && \
                    echo "Virtual environment created successfully" || \
                    { echo "Virtual environment creation failed"; exit 1; }
                    
                    echo "Verifying venv structure..."
                    ls -l ${VENV_DIR}/bin
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    echo "Activating virtual environment and installing dependencies..."
                    . ${VENV_DIR}/bin/activate && \
                    pip install --upgrade pip && \
                    pip install -e . && \
                    echo "Dependencies installed successfully" || \
                    { echo "Dependency installation failed"; exit 1; }
                '''
            }
        }
    }
}