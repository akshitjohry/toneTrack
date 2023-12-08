gcloud config set compute/zone us-central1-b
gcloud container clusters create mykube --preemptible --release-channel None --zone us-central1-b --enable-google-cloud-access
helm install -f ./minio-config.yaml -n minio-ns --create-namespace minio-proj bitnami/minio
kubectl port-forward --namespace minio-ns svc/minio-proj 9000:9000 &
kubectl port-forward --namespace minio-ns svc/minio-proj 9001:9001 &
kubectl create namespace mykube
kubectl create serviceaccount mykubeservice --namespace mykube
kubectl apply -f minio/minio-external-service.yaml
kubectl apply -f redis/redis-deployment.yaml
kubectl apply -f redis/redis-service.yaml
kubectl port-forward --address 0.0.0.0 --namespace mykube service/redis 6379:6379 &
kubectl apply -f rest/rest-deployment.yaml
kubectl apply -f rest/rest-service.yaml
kubectl port-forward --address 0.0.0.0 --namespace mykube service/rest 5000:5000 &
kubectl get all --namespace mykube
kubectl apply -f worker/worker-deployment.yaml
kubectl get all --namespace mykube
kubectl exec -it pod/emorecong-796bd985fc-l49lr --namespace mykube -- /bin/bash