#!/bin/bash
# Login to ECR so EC2 can pull the private image
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 559307249825.dkr.ecr.ap-south-1.amazonaws.com
