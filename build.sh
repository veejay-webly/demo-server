#!/bin/bash

CGO_ENABLED=0 go build
docker build -t demo/demo-server .
