package main

import (
	"RabbitMQ"
	"fmt"
	"strconv"
	"time"
)

func main() {
	rabbitmq := RabbitMQ.NewRabbitMQSimple("simple")
	for i := 0; i < 100; i++ {
		rabbitmq.PublishSimple("hello world! " + strconv.Itoa(i))
		time.Sleep(1 * time.Second)
		fmt.Println(i)
	}

}
