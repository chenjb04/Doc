package main

import "RabbitMQ"

func main() {
	rabbitmq := RabbitMQ.NewRabbitMQRouting("routing", "two")
	rabbitmq.ConsumeRouting()

}
