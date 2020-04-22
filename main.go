package main

import (
	"flag"
	"fmt"
	"net/http"
	"os"
	"time"

	log "github.com/sirupsen/logrus"
)

func main() {
	log.Info("demo-server starting ...")
	port := flag.String("port", "3001", "Specify port.")
	flag.Parse()

	if envPort := os.Getenv("PORT"); len(envPort) > 0 {
		*port = envPort
	}

	http.HandleFunc("/hi", handler)
	http.HandleFunc("/date", dateHandler)

	log.Infof("Server listening on port: %s", *port)
	log.Fatal(http.ListenAndServe(fmt.Sprintf(":%s", *port), nil))
}

func handler(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	fmt.Fprintln(w, "Hello from demo-server!")
}

func dateHandler(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	fmt.Fprintf(w, "%v\n", time.Now())
}
