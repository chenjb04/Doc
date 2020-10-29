package main

import "RabbitMQ"

func main() {
	rabbitmq := RabbitMQ.NewRabbitMQTopic("topic", "*.go")
	rabbitmq.ConsumeTopic()

}

