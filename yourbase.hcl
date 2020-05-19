service "demo-server" {
    buildpack "go" { version = "1.13.9" }

    setup {}

    build {
        commands = [
            "go get"
            "go build"
        ]
    }

    test {
        command = "go test ./..."
    }

    run {
        environment {
            variable "PORT" {
                value = "3002"
            }
        }
    }
}