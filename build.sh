#!/bin/sh
cd app && docker build . --tag todo-app
docker tag todo-app localhost:5001/todo-app
docker push localhost:5001/todo-app