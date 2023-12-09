#!/bin/sh
#
# You can use this script to launch Redis and minio on Kubernetes
# and forward their connections to your local computer. That means
# you can then work on your worker-server.py and rest-server.py
# on your local computer rather than pushing to Kubernetes with each change.
#
# To kill the port-forward processes us e.g. "ps augxww | grep port-forward"
# to identify the processes ids
#

gcloud container clusters get-credentials mykube
kubectl create namespace mykube
kubectl create serviceaccount mykubeservice --namespace mykube

kubectl apply -f minio/minio-external-service.yaml

kubectl apply -f redis/redis-deployment.yaml
kubectl apply -f redis/redis-service.yaml

kubectl port-forward --address 0.0.0.0 --namespace mykube service/redis 6379:6379 &

kubectl apply -f rest/rest-deployment.yaml

kubectl apply -f rest/rest-service.yaml
kubectl port-forward --address 0.0.0.0 --namespace mykube service/rest 5000:5000 &

kubectl apply -f worker/worker-deployment.yaml






# If you're using minio from the kubernetes tutorial this will forward those
# kubectl port-forward -n minio-ns --address 0.0.0.0 service/minio-proj 9000:9000 &
# kubectl port-forward -n minio-ns --address 0.0.0.0 service/minio-proj 9001:9001 &

while true; do kubectl port-forward --address 0.0.0.0 service/minio 9000:9000 & kubectl port-forward --address 0.0.0.0 service/minio 9001:9001; done &
