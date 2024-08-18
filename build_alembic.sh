#!/bin/sh
cd app && docker build -f Dockerfile.alembic . --tag todo-app-alembic
docker tag todo-app-alembic localhost:5001/todo-app-alembic
docker push localhost:5001/todo-app-alembic