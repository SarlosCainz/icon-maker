NAME := icon-maker
REGISTRY := sarlos

build: build-npm
#	cd ui && docker build -t ${REGISTRY}/${NAME}-web .
	docker build -t $(REGISTRY)/$(NAME)  .

build-test: build-npm
#	cd ui && docker build -t ${REGISTRY}/${NAME}-web:test .
	docker build -t $(REGISTRY)/$(NAME):test .

push:
#	docker push $(REGISTRY)/$(NAME)-web
	docker push $(REGISTRY)/$(NAME)

push-test:
#	docker push $(REGISTRY)/$(NAME)-web:test
	docker push $(REGISTRY)/$(NAME):test

build-npm:
	cd ui && npm run build

release:
	cd misc && make

clean:
	docker system prune -f
