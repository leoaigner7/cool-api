pipeline {
    agent any

    environment {
        IMAGE = "ghcr.io/${env.OWNER ?: "leoaigner7"}/${env.REPO ?: "cool-api"}:latest"
        COMPOSE_PATH = "/opt/cool-app/docker"
    }

    stages {
        stage('Pull latest image') {
            steps {
                sh '''
                    echo "🔹 Login to GHCR"
                    docker login ghcr.io -u '${OWNER:-leoaigner7}' -p $GITHUB_TOKEN
                    echo "🔹 Pull image: $IMAGE"
                    docker pull $IMAGE
                '''
            }
        }
        stage('Deploy with docker compose') {
            steps {
                sh '''
                    set -e
                    cd $COMPOSE_PATH
                    docker compose pull api
                    docker compose up -d api
                    docker image prune -f
                '''
            }
        }
    }
}

