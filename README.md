# Chatroom

Chatroom is web application that allows users to create temporary chatrooms, public or private, and communicate in real time. Public rooms are listed on the home page along with the number of users currently connected to them, private rooms are accesible only via link. Rooms can be created and used by both anonymous and registered users. Rooms can also be protected by password.
![App screenshot should appear here](https://i.imgur.com/Pcy7YP3.png)<br>

Backend for this application was created using Django, django-rest-framework and django/channels. It consists of 2 Django instances, one of which is responsible for handling HTTP traffic and the other handles Websocket communication.

Frontend was written in Angular and is the modified version of angular-realworld-example-app which can be found [here](https://github.com/gothinkster/angular-realworld-example-app).

All of the project components work behind nginx reverse proxy and entire project is dockerized.

## How to run

Easiest way to run the project is to use commands from `Makefile`. For example, to start project in development build:

```shell
make build-dev
make dev
```

List of all `make` commands:

- `build-dev` - build docker images of services in development environment
- `dev` - start project in development environment
- `build-prod` - build docker images of services in production environment
- `prod` - start project in production environment
- `test-backend` - run backend test suite
- `shell` - enter backend's Django shell

Of course you can also start the project by using docker-compose commands that sit behind `make` commands - e.g.

`docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build`
