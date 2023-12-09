VERSION=v5
DOCKERUSER=ajmo2266

build:
	docker build -t demucs-minio .

push:
	docker tag demucs-minio $(DOCKERUSER)/demucs-minio:$(VERSION)
	docker push $(DOCKERUSER)/demucs-minio:$(VERSION)
	docker tag demucs-minio $(DOCKERUSER)/demucs-minio:latest
	docker push $(DOCKERUSER)/demucs-minio:latest