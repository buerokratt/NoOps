IMAGE_NAME=custom-metrics-checker
CONTAINER_NAME=metrics-checker

.PHONY: build run logs clean compose-up compose-down

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run --rm --name $(CONTAINER_NAME) \
		-v /var/run/docker.sock:/var/run/docker.sock \
		-v $(PWD)/data:/data \
		$(IMAGE_NAME)

logs:
	cat ./data/metrics.log

clean:
	docker rmi $(IMAGE_NAME) || true

compose-up:
	docker-compose up --build -d

compose-down:
	docker-compose down
