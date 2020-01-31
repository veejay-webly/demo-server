FROM alpine:latest

WORKDIR /

ADD demo-server /

ENTRYPOINT ["/demo-server"]