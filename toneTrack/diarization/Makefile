VERSION=v13
DOCKERUSER=ajmo2266

build:
	docker build -f Dockerfile -t diarization .
push:
	docker tag diarization $(DOCKERUSER)/diarization:$(VERSION)
	docker push $(DOCKERUSER)/diarization:$(VERSION)
	docker tag diarization $(DOCKERUSER)/diarization:latest
	docker push $(DOCKERUSER)/diarization:latest
