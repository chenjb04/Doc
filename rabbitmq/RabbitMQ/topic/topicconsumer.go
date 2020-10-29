package main

import "RabbitMQ"

func main() {
	rabbitmq := RabbitMQ.NewRabbitMQTopic("topic", "#")
	rabbitmq.ConsumeTopic()

}
