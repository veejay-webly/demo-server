#!/bin/bash

commit=$(git rev-parse HEAD)
GOOS=linux CGO_ENABLED=0 go build
docker build -t jamesnaftel-demo-server:$commit . --label "org=jamesnaftel"
