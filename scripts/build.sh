#/bin/sh
set -e
git pull origin main
docker build -t auraska-base:14.0 -f BaseDockerfile .
docker build -t auraska:14.0 -f .
docker-compose down
docker-compose up -d
docker system prune -f
