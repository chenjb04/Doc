package main

import (
	"RabbitMQ"
	"fmt"
	"strconv"
	"time"
)

func main() {
	one := RabbitMQ.NewRabbitMQTopic("topic", "topic1.go")
	two := RabbitMQ.NewRabbitMQTopic("topic", "topic2")
	for i := 0; i < 10; i++ {
		one.PublishTopic("hello topic1 " + strconv.Itoa(i))
		two.PublishTopic("hello topic2 " + strconv.Itoa(i))
		time.Sleep(1 * time.Second)
		fmt.Println(i)
	}
}
