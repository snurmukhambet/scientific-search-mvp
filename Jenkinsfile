pipeline {
    agent any
    
    environment {
        BACKEND_IMAGE = "scientific-search-backend"
        GEMINI_API_KEY = credentials('gemini-api-key')
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                script {
                    env.GIT_COMMIT_SHORT = sh(
                        script: "git rev-parse --short HEAD",
                        returnStdout: true
                    ).trim()
                }
            }
        }
        
        stage('Backend Tests') {
            agent {
                docker {
                    image 'python:3.11-slim'
                    args '-u root'
                }
            }
            steps {
                dir('backend') {
                    sh '''
                        python -m pip install --upgrade pip
                        pip install -r requirements.txt
                    '''
                    sh 'python -m pytest tests/ -v'
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    def backendImage = docker.build("${BACKEND_IMAGE}:${env.GIT_COMMIT_SHORT}", "./backend")
                    backendImage.tag("latest")
                }
            }
        }
    }
    
    post {
        always {
            sh 'docker image prune -f'
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}