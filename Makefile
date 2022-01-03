NAME := icon-maker
REGISTRY := sarlos

build: build-npm
#	cd ui && docker build -t ${REGISTRY}/${NAME}-web .
	docker build -t $(REGISTRY)/$(NAME)  .

build-test: build-npm
#	cd ui && docker build -t ${REGISTRY}/${NAME}-web:test .
	docker build -t $(REGISTRY)/$(NAME):test .

push: build
#	docker push $(REGISTRY)/$(NAME)-web
	docker push $(REGISTRY)/$(NAME)

push-test: build-test
#	docker push $(REGISTRY)/$(NAME)-web:test
	docker push $(REGISTRY)/$(NAME):test

build-npm:
	cd ui && npm run build

clean:
	docker system prune -f
