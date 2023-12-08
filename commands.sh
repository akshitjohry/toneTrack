gcloud config set compute/zone us-central1-b
gcloud container clusters create mykube --preemptible --release-channel None --zone us-central1-b --enable-google-cloud-access
helm install -f ./minio-config.yaml -n minio-ns --create-namespace minio-proj bitnami/minio
kubectl port-forward --namespace minio-ns svc/minio-proj 9000:9000 &
kubectl port-forward --namespace minio-ns svc/minio-proj 9001:9001 &
gcloud container clusters get-credentials mykube
kubectl create namespace mykube
kubectl create serviceaccount mykubeservice --namespace mykube
gcloud iam service-accounts create mykubesa3 --project=blume-384702
gcloud projects add-iam-policy-binding blume-384702 --member "serviceAccount:mykubesa@blume-384702.iam.gserviceaccount.com" --role roles/speech.admin
gcloud container clusters update mykube --workload-pool=blume-384702.svc.id.goog
gcloud iam service-accounts add-iam-policy-binding mykubesa@blume-384702.iam.gserviceaccount.com --member "serviceAccount:blume-384702.svc.id.goog[mykube/mykubeservice]" --role roles/compute.admin
kubectl annotate serviceaccount mykubeservice --namespace mykube iam.gke.io/gcp-service-account=mykubesa@blume-384702.iam.gserviceaccount.com
kubectl port-forward --namespace minio-ns svc/minio-proj 9000:9000 &
kubectl port-forward --namespace minio-ns svc/minio-proj 9001:9001 &
cd toneTrack/toneTrack/
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