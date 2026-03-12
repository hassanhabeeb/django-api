#!/bin/bash
cd /home/django-api/
# Pull the latest image we just pushed in CodeBuild
docker-compose pull
# Restart the containers with the new image
docker-compose up -d --remove-orphans
