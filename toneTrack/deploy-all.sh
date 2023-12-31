#!/bin/sh
kubectl apply -f redis/redis-deployment.yaml
kubectl apply -f redis/redis-service.yaml

kubectl apply -f rest/rest-deployment.yaml
kubectl apply -f rest/rest-ingress.yaml

kubectl apply -f logs/logs-deployment.yaml


kubectl apply -f diarization/worker-deployment.yaml
kubectl apply -f emotion/worker-deployment.yaml

kubectl apply -f minio/minio-external-service.yaml
