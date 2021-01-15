build-dev:
	docker-compose build

dev:
	docker-compose up

shell:
	docker-commpose exec backend python manage.py shell
