package main

import (
	"RabbitMQ"
	"fmt"
	"strconv"
)

func main() {
	rabbitmq := RabbitMQ.NewRabbitMQSimple("simple")
	for i := 0; i < 10; i++ {
		rabbitmq.PublishSimple("hello world! " + strconv.Itoa(i))
	}

	fmt.Println("发送成功")
}
