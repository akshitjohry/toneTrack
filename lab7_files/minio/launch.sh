helm repo add bitnami https://charts.bitnami.com/bitnami

helm install -f ./minio-config.yaml -n minio-ns --create-namespace minio-proj bitnami/minio

kubectl port-forward --namespace minio-ns svc/minio-proj 9001:9001 &