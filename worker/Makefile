VERSION=v7
DOCKERUSER=ajmo2266

build:
	docker build -f Dockerfile -t emorecong .
push:
	docker tag emorecong $(DOCKERUSER)/emorecong:$(VERSION)
	docker push $(DOCKERUSER)/emorecong:$(VERSION)
	docker tag emorecong $(DOCKERUSER)/emorecong:latest
	docker push $(DOCKERUSER)/emorecong:latest
