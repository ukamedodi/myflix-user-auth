pipeline {
    agent any

    environment {
        PROD_USERNAME = 'ukamedodi'
        PROD_SERVER = '34.130.249.80'
        PROD_DIR = '/home/ukamedodi/myflix-user-auth'
        DOCKER_IMAGE_NAME = 'userAuth-deployment'
        DOCKER_CONTAINER_NAME = 'userAuth'
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
                    sh 'tar -czf userAuth.tar.gz *'
                    sh "scp -o StrictHostKeyChecking=no userAuth.tar.gz ${PROD_USERNAME}@${PROD_SERVER}:${PROD_DIR}"
                    sh 'echo Files transferred'
                    sh "ssh -o StrictHostKeyChecking=no ${PROD_USERNAME}@${PROD_SERVER} 'pwd && cd myflix-user-auth && tar -xzf userAuth.tar.gz && ls -l'"
                    
                }
            }
        }

        stage('Dockerize DB Application') {
            steps {
                script {
                    sh "ssh -o StrictHostKeyChecking=no ${PROD_USERNAME}@${PROD_SERVER} 'cd myflix-user-auth && docker build -t ${DOCKER_IMAGE_NAME} .'"
                    sh "echo Docker image for userAuth rebuilt. Preparing to redeploy container to web..."
                }
            }
        }

        stage('Redeploy Container') {
            steps {
                script {
                    sh "ssh -o StrictHostKeyChecking=no ${PROD_USERNAME}@${PROD_SERVER} 'cd myflix-user-auth && docker stop ${DOCKER_CONTAINER_NAME} || true'"
                    sh "ssh -o StrictHostKeyChecking=no ${PROD_USERNAME}@${PROD_SERVER} 'cd myflix-user-auth && docker rm ${DOCKER_CONTAINER_NAME} || true'"
                    sh "echo Container stopped and removed. Preparing to redeploy new version"

                    sh "ssh -o StrictHostKeyChecking=no ${PROD_USERNAME}@${PROD_SERVER} 'cd myflix-user-auth && docker run -d -p ${DOCKER_HOST_PORT}:${DOCKER_CONTAINER_PORT} --name ${DOCKER_CONTAINER_NAME} ${DOCKER_IMAGE_NAME}'"
                    sh "echo userAuth Microservice Deployed!"
                }
            }
        }
    }
}
