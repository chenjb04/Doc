package main

import "RabbitMQ"

func main() {
	rabbitmq := RabbitMQ.NewRabbitMQSimple("simple")
	rabbitmq.ConsumeSimple()
}
