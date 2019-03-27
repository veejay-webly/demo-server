package main

import (
	"flag"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"
)

func main() {
	port := flag.String("port", "3001", "Specify port to use")
	flag.Parse()

	if envPort := os.Getenv("PORT"); len(envPort) > 0 {
		*port = envPort
	}

	http.HandleFunc("/hi", handler)
	http.HandleFunc("/date", dateHandler)

	log.Fatal(http.ListenAndServe(fmt.Sprintf(":%s", *port), nil))
}

func handler(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	fmt.Fprintln(w, "Hello!")
}

func dateHandler(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	fmt.Fprintf(w, "%v\n", time.Now())
}
