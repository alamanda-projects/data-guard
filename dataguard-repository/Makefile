MONGODB_USER ?= admin
MONGODB_PASS ?= yellow

docker_build_app_image:
	docker build \
		-f infra/python/Dockerfile \
		-t dgr-app-image:latest .

docker_build_db_image:
	docker build \
		-f infra/mongodb/Dockerfile \
		--build-arg MONGODB_USER=$(MONGODB_USER) \
		--build-arg MONGODB_PASS=$(MONGODB_PASS) \
		-t dgr-db-image:latest .

docker_compose_up:
	docker compose up --build -d  

docker_remove_dangling_images:
	docker image prune -f

docker_create_network:
	docker network inspect exa-net >/dev/null 2>&1 || docker network create exa-net

service_stop:
	docker compose down -v

service_start: docker_build_app_image \
	docker_build_db_image \
	docker_create_network \
	docker_compose_up \
	docker_remove_dangling_images

copy_env_file:
	cp app/.env.example app/.env
