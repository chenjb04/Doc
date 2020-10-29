package main

import "RabbitMQ"

func main() {
	rabbitmq := RabbitMQ.NewRabbitMQRouting("routing", "one")
	rabbitmq.ConsumeRouting()

}
