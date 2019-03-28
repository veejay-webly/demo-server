image:
	docker run --name demo-server-container golang go get -v github.com/jamesnaftel/demo-server/...
	docker commit demo-server-container jamesnaftel/demo

run:
	docker run --rm -d -p 8081:3001 jamesnaftel/demo demo-server

clean:
	docker rm demo-server-container
	docker rmi jamesnaftel/demo

