#!/bin/sh
kubectl delete -f redis/redis-deployment.yaml
kubectl delete -f redis/redis-service.yaml

kubectl delete -f rest/rest-deployment.yaml
kubectl delete -f rest/rest-ingress.yaml

kubectl delete -f logs/logs-deployment.yaml

kubectl delete -f worker/worker-deployment.yaml

kubectl delete -f minio/minio-external-service.yaml
