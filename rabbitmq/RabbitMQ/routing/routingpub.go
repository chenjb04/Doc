package main

import (
	"RabbitMQ"
	"fmt"
	"strconv"
	"time"
)

func main() {
	one := RabbitMQ.NewRabbitMQRouting("routing", "one")
	two := RabbitMQ.NewRabbitMQRouting("routing", "two")
	for i := 0; i < 10; i++ {
		one.PublishRouting("hello " + strconv.Itoa(i))
		two.PublishRouting("hello " + strconv.Itoa(i))
		time.Sleep(1 * time.Second)
		fmt.Println(i)
	}
}