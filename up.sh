#!/bin/bash
docker-compose -f docker/docker-compose.dev.yml -p PROJECT up -d --build
docker exec -it PROJECT-dev-1 /bin/sh
