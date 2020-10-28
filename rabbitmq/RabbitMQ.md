# RabbitMQ

## 使用场景

```
程序解耦
流量削峰
异步处理
```

## 安装

docker安装

```shell
docker pull rabbitmq
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 --hostname my-rabbitmq  -e RABBITMQ_DEFAULT_USER=admin -e RABBITMQ_DEFAULT_PASS=admin rabbitmq
```

启动web管理页面

```shell
 docker exec -it rabbitmq /bin/bash
 rabbitmq-plugins enable rabbitmq_management
```

浏览器输入`http://ip:15672`即可访问web管理页面。

## 核心概念

模型架构图

![image-20201027211530636](C:\Users\vt\AppData\Roaming\Typora\typora-user-images\image-20201027211530636.png)

- publisher:生产者，负责生产消息并将其投递到指定的交换器上。
- message：消息，消息由消息头和消息体组成。消息头用于存储与消息相关的元数据：如目标交换器的名字 (exchange_name) 、路由键 (RountingKey)
  和其他可选配置 (properties) 信息。消息体为实际需要传递的数据。
- connection：用于传递消息的TCP连接。
- channel:消息通道，在客户端的每个连接里，可建立多个channel，每个channel代表一个会话任务。
- exchange:消息交换机，它指定消息按什么规则路由到哪个队列。
- bindingkey：交换器与队列通过 BindingKey 建立绑定关系。
- queue:消息队列载体，每个消息都会被投入到一个或多个队列。
- virtual host:RabbitMQ 通过虚拟主机来实现逻辑分组和资源隔离，一个虚拟主机就是一个小型的 RabbitMQ
  服务器，拥有独立的队列、交换器和绑定关系。用户可以按照不同业务场景建立不同的虚拟主机，虚拟主机之间是完全独立的，你无法将 vhost1 上的交换器与vhost 上的队列进行绑定，这可以极大的保证业务之间的隔离性和数据安全。默认的虚拟主机名为 `/` 。
- consumer:消费者

## 工作模式

### simple模式

即一个生产者，一个消费者。

生产者将消息交给默认的交换机，交换机获取消息后交给绑定这个生产者的队列（投递规则为队列名称和routing key 相同的队列），监听当前队列的消费者获取信息并执行消费逻辑。

示例：

```go
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

//创建RabbitMQ实例
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

```

使用：

```go
//生产者
func main() {
	rabbitmq := RabbitMQ.NewRabbitMQSimple("simple")
	for i := 0; i < 10; i++ {
		rabbitmq.PublishSimple("hello world! " + strconv.Itoa(i))
	}

	fmt.Println("发送成功")
}

//消费者
func main() {
	rabbitmq := RabbitMQ.NewRabbitMQSimple("simple")
	rabbitmq.ConsumeSimple()
}
```

分别运行生产者和消费者

```
2020/10/28 16:59:36 [x] send hello world! 0
2020/10/28 16:59:36 [x] send hello world! 1
2020/10/28 16:59:36 [x] send hello world! 2
2020/10/28 16:59:36 [x] send hello world! 3
2020/10/28 16:59:36 [x] send hello world! 4
2020/10/28 16:59:36 [x] send hello world! 5
2020/10/28 16:59:36 [x] send hello world! 6
2020/10/28 16:59:36 [x] send hello world! 7
2020/10/28 16:59:36 [x] send hello world! 8
2020/10/28 16:59:36 [x] send hello world! 9
发送成功


2020/10/28 16:37:06 [*] waiting for message, To exit press Ctrl + C
2020/10/28 16:59:36 received a message:hello world! 0
2020/10/28 16:59:36 received a message:hello world! 1
2020/10/28 16:59:36 received a message:hello world! 2
2020/10/28 16:59:36 received a message:hello world! 3
2020/10/28 16:59:36 received a message:hello world! 4
2020/10/28 16:59:36 received a message:hello world! 5
2020/10/28 16:59:36 received a message:hello world! 6
2020/10/28 16:59:36 received a message:hello world! 7
2020/10/28 16:59:36 received a message:hello world! 8
2020/10/28 16:59:36 received a message:hello world! 9
```

### work模式

