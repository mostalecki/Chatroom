#!/usr/bin/env bash

until nc -z $POSTGRES_HOST $POSTGRES_PORT
do
  echo Waiting for db...
  sleep 1
done

echo Connected with database
