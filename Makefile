build-dev:
	docker-compose build

dev:
	docker-compose up

build-prod:
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml build

prod:
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up

test-backend:
	docker-compose exec backend pytest

shell:
	docker-compose exec backend python manage.py shell
