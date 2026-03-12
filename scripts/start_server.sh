#!/bin/bash
cd /home/django-api/
# Login to ECR
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 559307249825.dkr.ecr.ap-south-1.amazonaws.com
# Pull and Restart
docker compose pull
docker compose up -d --force-recreate --remove-orphans
