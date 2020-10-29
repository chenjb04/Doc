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

一个生产者，多个消费者，每个消费者获取到的消息唯一，一个消息只能被消费一次，场景适用于负载均衡，当生产者速度大于消费者时。

示例：

生产者

```go
func main() {
	rabbitmq := RabbitMQ.NewRabbitMQSimple("simple")
	for i := 0; i < 100; i++ {
		rabbitmq.PublishSimple("hello world! " + strconv.Itoa(i))
		time.Sleep(1 * time.Second)
		fmt.Println(i)
	}

}
```

消费者1

```go
func main() {
	rabbitmq := RabbitMQ.NewRabbitMQSimple("simple")
	rabbitmq.ConsumeSimple()
}

```

消费者2

```go
func main() {
	rabbitmq := RabbitMQ.NewRabbitMQSimple("simple")
	rabbitmq.ConsumeSimple()
}

```

结果

```go
// 消费者1
2020/10/28 20:35:44 [*] waiting for message, To exit press Ctrl + C
2020/10/28 20:36:01 received a message:hello world! 0
2020/10/28 20:36:03 received a message:hello world! 2
2020/10/28 20:36:06 received a message:hello world! 4
2020/10/28 20:36:08 received a message:hello world! 6
2020/10/28 20:36:10 received a message:hello world! 8
2020/10/28 20:36:12 received a message:hello world! 10
...
//消费者2
2020/10/28 20:35:51 [*] waiting for message, To exit press Ctrl + C
2020/10/28 20:36:02 received a message:hello world! 1
2020/10/28 20:36:04 received a message:hello world! 3
2020/10/28 20:36:07 received a message:hello world! 5
2020/10/28 20:36:09 received a message:hello world! 7
2020/10/28 20:36:11 received a message:hello world! 9
2020/10/28 20:36:13 received a message:hello world! 11
...
```

### 订阅模式

一条消息可以被多个消费者消费

示例：

创建实例

```go
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
```

生产者

```go
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
```

消费者

```go
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
	messages, err := r.channel.Consume(q.Name, "", true, false,  false, false, nil)
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

使用

```go
// 生产者
func main() {
	rabbitmq := RabbitMQ.NewRabbitMQPubSub("newProduct")
	for i := 0; i < 10; i++ {
		rabbitmq.PublishPub("订阅模式生产第" + strconv.Itoa(i) + "条数据")
		fmt.Println("订阅模式生产第" + strconv.Itoa(i) + "条数据")
		time.Sleep(1 * time.Second)
	}
}
//消费者1
func main() {
	rabbitmq := RabbitMQ.NewRabbitMQPubSub("newProduct")
	rabbitmq.ConsumeSub()
}
//消费者2
func main() {
	rabbitmq := RabbitMQ.NewRabbitMQPubSub("newProduct")
	rabbitmq.ConsumeSub()
}
```

结果

```go
//生产者
订阅模式生产第0条数据
订阅模式生产第1条数据
订阅模式生产第2条数据
订阅模式生产第3条数据
订阅模式生产第4条数据
订阅模式生产第5条数据
订阅模式生产第6条数据
订阅模式生产第7条数据
订阅模式生产第8条数据
订阅模式生产第9条数据
//消费者1
2020/10/29 15:37:07 [*] waiting for message, To exit press Ctrl + C
2020/10/29 15:37:14 received a message:订阅模式生产第0条数据
2020/10/29 15:37:15 received a message:订阅模式生产第1条数据
2020/10/29 15:37:16 received a message:订阅模式生产第2条数据
2020/10/29 15:37:17 received a message:订阅模式生产第3条数据
2020/10/29 15:37:18 received a message:订阅模式生产第4条数据
2020/10/29 15:37:19 received a message:订阅模式生产第5条数据
2020/10/29 15:37:20 received a message:订阅模式生产第6条数据
2020/10/29 15:37:21 received a message:订阅模式生产第7条数据
2020/10/29 15:37:22 received a message:订阅模式生产第8条数据
2020/10/29 15:37:23 received a message:订阅模式生产第9条数据
//消费者2
2020/10/29 15:37:11 [*] waiting for message, To exit press Ctrl + C
2020/10/29 15:37:14 received a message:订阅模式生产第0条数据
2020/10/29 15:37:15 received a message:订阅模式生产第1条数据
2020/10/29 15:37:16 received a message:订阅模式生产第2条数据
2020/10/29 15:37:17 received a message:订阅模式生产第3条数据
2020/10/29 15:37:18 received a message:订阅模式生产第4条数据
2020/10/29 15:37:19 received a message:订阅模式生产第5条数据
2020/10/29 15:37:20 received a message:订阅模式生产第6条数据
2020/10/29 15:37:21 received a message:订阅模式生产第7条数据
2020/10/29 15:37:22 received a message:订阅模式生产第8条数据
2020/10/29 15:37:23 received a message:订阅模式生产第9条数据
```

### 路由模式

一个消息可以被多个消费者消费。并且消息的目标队列可被生产者指定。

示例：

创建实例：

```go
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
```

生产者

```go
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
```

消费者

```go
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
```

使用

```go
//生产者
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
//消费者1
func main() {
	rabbitmq := RabbitMQ.NewRabbitMQRouting("routing", "one")
	rabbitmq.ConsumeRouting()

}

//消费者2
func main() {
	rabbitmq := RabbitMQ.NewRabbitMQRouting("routing", "two")
	rabbitmq.ConsumeRouting()

}
```

结果

```go
//消费者1
2020/10/29 16:29:25 [*] waiting for message, To exit press Ctrl + C
2020/10/29 16:29:28 received a message:hello 0 from one
2020/10/29 16:29:29 received a message:hello 1 from one
2020/10/29 16:29:30 received a message:hello 2 from one
2020/10/29 16:29:31 received a message:hello 3 from one
2020/10/29 16:29:33 received a message:hello 4 from one
2020/10/29 16:29:34 received a message:hello 5 from one
2020/10/29 16:29:35 received a message:hello 6 from one
2020/10/29 16:29:36 received a message:hello 7 from one
2020/10/29 16:29:37 received a message:hello 8 from one
2020/10/29 16:29:38 received a message:hello 9 from one
//消费者2
2020/10/29 16:29:23 [*] waiting for message, To exit press Ctrl + C
2020/10/29 16:29:28 received a message:hello 0 from two
2020/10/29 16:29:29 received a message:hello 1 from two
2020/10/29 16:29:30 received a message:hello 2 from two
2020/10/29 16:29:32 received a message:hello 3 from two
2020/10/29 16:29:33 received a message:hello 4 from two
2020/10/29 16:29:34 received a message:hello 5 from two
2020/10/29 16:29:35 received a message:hello 6 from two
2020/10/29 16:29:36 received a message:hello 7 from two
2020/10/29 16:29:37 received a message:hello 8 from two
2020/10/29 16:29:38 received a message:hello 9 from two
```

