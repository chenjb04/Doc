package main

import "RabbitMQ"

func main() {
	rabbitmq := RabbitMQ.NewRabbitMQPubSub("newProduct")
	rabbitmq.ConsumeSub()
}
