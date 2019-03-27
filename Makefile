image:
	docker run --name demo-server-container golang go get -v github.com/jamesnaftel/demo-server/...
	docker commit demo-server-container demo

run:
	docker run --rm -p 8081:3001 demo demo-server

clean:
	docker rm demo-server-container
	docker rmi demo

