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