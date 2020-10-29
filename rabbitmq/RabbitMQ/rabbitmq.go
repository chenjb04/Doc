package RabbitMQ

import (
	"fmt"
	"github.com/streadway/amqp"
	"log"
)

// 连接格式：amqp://用户名:密码@rabbitmq服务地址:端口/vhost
const MqUrl = "amqp://admin:admin@39.106.88.184:5672/"

type RabbitMQ struct {
	// 连接
	conn *amqp.Connection
	// 通道
	channel *amqp.Channel
	// 队列名称
	QueueName string
	// 交换机
	Exchange string
	// key
	Key string
	// 连接MqUrl
	MqUrl string
}

//创建简单模式RabbitMQ实例
func NewRabbitMQ(queueName string, exchange string, key string) *RabbitMQ {
	rabbitmq := &RabbitMQ{QueueName: queueName, Exchange: exchange, Key: key, MqUrl: MqUrl}
	// 创建连接
	var err error
	rabbitmq.conn, err = amqp.Dial(rabbitmq.MqUrl)
	rabbitmq.failOnError(err, "创建连接错误")
	rabbitmq.channel, err = rabbitmq.conn.Channel()
	rabbitmq.failOnError(err, "获取channel失败")
	return rabbitmq
}

// 断开连接
func (r *RabbitMQ) Destroy() {
	var err error
	err = r.channel.Close()
	r.failOnError(err, "关闭channel错误")
	err = r.conn.Close()
	r.failOnError(err, "关闭连接错误")
}

// 错误处理
func (r *RabbitMQ) failOnError(err error, message string) {
	if err != nil {
		log.Fatalf("%s:%s", message, err)
		//panic(fmt.Sprintf("%s:%s", message, err))
	}
}

//simple模式
func NewRabbitMQSimple(queueName string) *RabbitMQ {
	return NewRabbitMQ(queueName, "", "")
}

// simple模式生产者
func (r *RabbitMQ) PublishSimple(message string) {
	//1.申请队列，队列不存在会自动创建
	// durable 是否持久化,autoDelete 是否自动删除, exclusive 是否具有排他性, noWait 是否阻塞
	//var err error
	_, err := r.channel.QueueDeclare(r.QueueName, false, false, false, false, nil)
	if err != nil {
		fmt.Println(err)
	}
	// 2.发送消息
	// mandatory 如果为True，会根据exchange类型和routKey规则，如果无法找到符合条件的队列，会把消息返回给生产者
	//immediate 如果为True，当exchange发送消息到队列后发现队列上没有绑定消费者，把消息返回给生产者
	err = r.channel.Publish(r.Exchange, r.QueueName, false, false, amqp.Publishing{
		ContentType: "text/plain", Body: []byte(message),
	})
	if err != nil {
		fmt.Println(err)
	}
	log.Printf("[x] send %s", message)

}

// simple模式消费者
func (r *RabbitMQ) ConsumeSimple() {
	//1.申请队列，队列不存在会自动创建
	// durable 是否持久化,autoDelete 是否自动删除, exclusive 是否具有排他性, noWait 是否阻塞
	//var err error
	_, err := r.channel.QueueDeclare(r.QueueName, false, false, false, false, nil)
	r.failOnError(err, "failed to declare queue")
	// 2.接收消息
	// consumer 用来区分多个消费者 autoAck 是否自动应答 noLocal 如果为True，表示不能将同一个connection中发送的消息传递给这个connection中的消费者
	messages, err := r.channel.Consume(r.QueueName, "", true, false, false, false, nil)
	r.failOnError(err, "failed to register a consumer")

	// 3。消费消息
	forever := make(chan bool)
	// 启用协程消费
	go func() {
		for d := range messages {
			log.Printf("received a message:%s", d.Body)
		}
	}()
	log.Printf("[*] waiting for message, To exit press Ctrl + C")
	<-forever
}

//创建订阅模式RabbitMQ示例
func NewRabbitMQPubSub(exchangeName string) *RabbitMQ {
	// 创建RabbitMQ示例
	rabbitmq := NewRabbitMQ("", exchangeName, "")
	var err error
	rabbitmq.conn, err = amqp.Dial(rabbitmq.MqUrl)
	rabbitmq.failOnError(err, "failed to connect to rabbit")
	rabbitmq.channel, err = rabbitmq.conn.Channel()
	rabbitmq.failOnError(err, "failed to open a channel")
	return rabbitmq
}

// 订阅模式生产者
func (r *RabbitMQ) PublishPub(message string) {
	//尝试创建交换机
	// kind 交换机类型 durable 是否持久化 autoDelete 是否自动删除 internal true表示这个exchange不可以被client用来推送消息，仅用来进行exchange之间的绑定
	// nowait 是否阻塞
	err := r.channel.ExchangeDeclare(r.Exchange, "fanout", true, false, false, false, nil)
	r.failOnError(err, "failed to declare an exchange")
	// 发送消息
	err = r.channel.Publish(r.Exchange, "", false, false, amqp.Publishing{
		ContentType: "text/plain", Body: []byte(message),
	})

}

//订阅模式消费者
func (r *RabbitMQ) ConsumeSub() {
	//试探性创建交换机
	err := r.channel.ExchangeDeclare(r.Exchange, "fanout", true, false, false, false, nil)
	r.failOnError(err, "failed to declare an exchange")
	//创建队列
	q, err := r.channel.QueueDeclare("", false, false, true, false, nil)
	r.failOnError(err, "failed to declare an queue")
	//绑定队列到exchange
	err = r.channel.QueueBind(q.Name, "", r.Exchange, false, nil)
	r.failOnError(err, "build failed")
	//消费消息
	messages, err := r.channel.Consume(q.Name, "", true, false, false, false, nil)
	forever := make(chan bool)
	// 启用协程消费
	go func() {
		for d := range messages {
			log.Printf("received a message:%s", d.Body)
		}
	}()
	log.Printf("[*] waiting for message, To exit press Ctrl + C")
	<-forever

}


// 路由模式创建RabbitMQ实例
func NewRabbitMQRouting(exchangeName string, routingKey string) *RabbitMQ {
	rabbitmq := NewRabbitMQ("", exchangeName, routingKey)
	var err error
	rabbitmq.conn, err = amqp.Dial(rabbitmq.MqUrl)
	rabbitmq.failOnError(err, "failed to connect to rabbit")
	rabbitmq.channel, err = rabbitmq.conn.Channel()
	rabbitmq.failOnError(err, "failed to open a channel")
	return rabbitmq
}

//路由模式生产者
func (r *RabbitMQ) PublishRouting(message string) {
	//创建交换机
	err := r.channel.ExchangeDeclare(r.Exchange, "direct", true, false, false, false, nil)
	r.failOnError(err, "failed to declare an exchange")
	//发送消息
	err = r.channel.Publish(r.Exchange, r.Key, false, false, amqp.Publishing{
		ContentType: "text/plain", Body: []byte(message),
	})
}

//路由模式消费者
func (r *RabbitMQ) ConsumeRouting() {
	//试探性创建交换机
	err := r.channel.ExchangeDeclare(r.Exchange, "direct", true, false, false, false, nil)
	r.failOnError(err, "failed to declare an exchange")
	//创建队列
	q, err := r.channel.QueueDeclare("", false, false, true, false, nil)
	r.failOnError(err, "failed to declare an queue")
	//绑定队列到exchange
	err = r.channel.QueueBind(q.Name, r.Key, r.Exchange, false, nil)
	r.failOnError(err, "build failed")
	//消费消息
	messages, err := r.channel.Consume(q.Name, "", true, false, false, false, nil)
	forever := make(chan bool)
	// 启用协程消费
	go func() {
		for d := range messages {
			log.Printf("received a message:%s from %s", d.Body, r.Key)
		}
	}()
	log.Printf("[*] waiting for message, To exit press Ctrl + C")
	<-forever

}

//topic模式创建实例
func NewRabbitMQTopic(exchange string,  routingKey string) *RabbitMQ{
	rabbitmq := NewRabbitMQ("", exchange, routingKey)
	var err error
	rabbitmq.conn, err = amqp.Dial(rabbitmq.MqUrl)
	rabbitmq.failOnError(err, "failed to connect to rabbit")
	rabbitmq.channel, err = rabbitmq.conn.Channel()
	rabbitmq.failOnError(err, "failed to open a channel")
	return rabbitmq
}

//topic模式生产者
func (r *RabbitMQ) PublishTopic(message string) {
	//创建交换机
	err := r.channel.ExchangeDeclare(r.Exchange, "topic", true, false, false, false, nil)
	r.failOnError(err, "failed to declare an exchange")
	//发送消息
	err = r.channel.Publish(r.Exchange, r.Key, false, false, amqp.Publishing{
		ContentType: "text/plain", Body: []byte(message),
	})
}

//topic模式消费者
func (r *RabbitMQ) ConsumeTopic() {
	//试探性创建交换机
	err := r.channel.ExchangeDeclare(r.Exchange, "topic", true, false, false, false, nil)
	r.failOnError(err, "failed to declare an exchange")
	//创建队列
	q, err := r.channel.QueueDeclare("", false, false, true, false, nil)
	r.failOnError(err, "failed to declare an queue")
	//绑定队列到exchange
	err = r.channel.QueueBind(q.Name,r.Key, r.Exchange, false, nil)
	r.failOnError(err, "build failed")
	//消费消息
	messages, err := r.channel.Consume(q.Name, "", true, false, false, false, nil)
	forever := make(chan bool)
	// 启用协程消费
	go func() {
		for d := range messages {
			log.Printf("received a message:%s", d.Body)
		}
	}()
	log.Printf("[*] waiting for message, To exit press Ctrl + C")
	<-forever
}
