pipeline {
    agent any

    environment {
        PROD_USERNAME = 'ukamedodi'
        PROD_SERVER = '34.130.249.80'
        PROD_DIR = '/home/ukamedodi/myflix-user-auth'
        DOCKER_IMAGE_NAME = 'myflix-deployment'
        DOCKER_CONTAINER_NAME = 'myflix'
        DOCKER_CONTAINER_PORT = '5000'
        DOCKER_HOST_PORT = '5000'
    }

    stages {
        stage('Load Code to Workspace') {
            steps {
                checkout scm             
            }
        }

        stage('Deploy Repo to Prod. Server') {
            steps {
                script {
                    sh 'echo Packaging files ...'
                    sh 'tar -czf myFlix.tar.gz *'
                    sh "scp -o StrictHostKeyChecking=no myFlix.tar.gz ${PROD_USERNAME}@${PROD_SERVER}:${PROD_DIR}"
                    sh 'echo Files transferred to server. Unpacking ...'
                    sh "ssh -o StrictHostKeyChecking=no ${PROD_USERNAME}@${PROD_SERVER} 'pwd && cd myflix && tar -xzf myFlix.tar.gz && ls -l'"
                    sh 'echo Repo unloaded on Prod. Server. Preparing to dockerize application ..'
                }
            }
        }

        stage('Dockerize DB Application') {
            steps {
                script {
                    sh "ssh -o StrictHostKeyChecking=no ${PROD_USERNAME}@${PROD_SERVER} 'cd myflix && docker build -t ${DOCKER_IMAGE_NAME} .'"
                    sh "echo Docker image for myFlix rebuilt. Preparing to redeploy container to web..."
                }
            }
        }

        stage('Redeploy Container') {
            steps {
                script {
                    sh "ssh -o StrictHostKeyChecking=no ${PROD_USERNAME}@${PROD_SERVER} 'cd myflix && docker stop ${DOCKER_CONTAINER_NAME} || true'"
                    sh "ssh -o StrictHostKeyChecking=no ${PROD_USERNAME}@${PROD_SERVER} 'cd myflix && docker rm ${DOCKER_CONTAINER_NAME} || true'"
                    sh "echo Container stopped and removed. Preparing to redeploy new version"

                    sh "ssh -o StrictHostKeyChecking=no ${PROD_USERNAME}@${PROD_SERVER} 'cd myflix && docker run -d -p ${DOCKER_HOST_PORT}:${DOCKER_CONTAINER_PORT} --name ${DOCKER_CONTAINER_NAME} ${DOCKER_IMAGE_NAME}'"
                    sh "echo myFlix Microservice Deployed!"
                }
            }
        }
    }
}
