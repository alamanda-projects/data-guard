docker_build_app_image:
	docker build -f infra/python/Dockerfile -t dcr-app-image:latest .

docker_build_db_image:
	docker build -f infra/mongodb/Dockerfile -t dcr-db-image:latest .

docker_compose_up:
	docker compose up --build -d  

docker_remove_dangling_images:
	docker image prune -f

docker_create_network:
	docker network inspect exa-net >/dev/null 2>&1 || docker network create exa-net

service_stop:
	docker compose down -v

service_start: docker_build_app_image docker_build_db_image docker_create_network \
docker_compose_up docker_remove_dangling_images

copy_env_file:
	cp app/.env.example app/.env
