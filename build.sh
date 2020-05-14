#!/bin/bash

commit=$(git rev-parse HEAD)
GOOS=linux CGO_ENABLED=0 go build
docker build -t jamesnaftel-demo-server:$commit .

docker tag jamesnaftel-demo-server:$commit docker-registry.yourbase.io/jamesnaftel-demo-server:$commit
docker push docker-registry.yourbase.io/jamesnaftel-demo-server:$commit
