# Chatroom
Chatroom is web application that allows it's users to create temporary chatrooms, public or private. Public rooms are listed on the main page along with the number of users currently connected to them, private rooms are accesible only via link. Rooms can be created and used by both anonymous and registered users. Registered users have the privilege of picking their username and setting custom avatar.
![App screenshot should appear here](https://i.imgur.com/MLo3emw.png)<br>

It was created using Django and Django Channels.
## How to run
1. Install all the packages from requirements.txt
2. Make sure you have created Postgres database and provided settings.py with credentials (or use other database, no postgres-only fields were used)
3. Run migrations with :
```shell
python manage.py migrate
```
4. Have Redis running at port 6379 (or some other, remember to change it in settings.py). Redis acts as backend to websocket channel layer. Easiest done via docker
```shell
docker run -p 6379:6379 -d redis:2.8
```
5. Run the server with
```shell
python manage.py runserver
```
