学习笔记

## Redis
- [Redis 官网文档](https://redis.io/documentation)

1. 生成测试数据
   $ pip3 install fake2db redis
   $ fake2db --rows 10000 --host 127.0.0.1 --db redis


2. [Redis-cli 命令参考](http://doc.redisfans.com/index.html)
  $ redis-cli -h host -p port -a password


<br/>

## Rabbitmq
1. 概念
```
    Brocker		：消息队列服务器实体
    Exchange	：消息交换机，指定消息按什么规则，路由到哪个队列。 默认的 exchange 是direct；
    Queue		：消息队列，每个消息都会被投入到一个或者多个队列里。
    Binding		：绑定，它的作用是把exchange和queue按照路由规则binding起来。
    Routing Key	：路由关键字，exchange根据这个关键字进行消息投递。
    Vhost		：虚拟主机，一个broker里可以开设多个vhost，用作不用用户的权限分离。
    Producer	：消息生产者，就是投递消息的程序。
    Consumer	：消息消费者，就是接受消息的程序。
    Channel		：消息通道，在客户端的每个连接里，可建立多个channel，每个channel代表一个会话任务。
```

2. Python pika
- [Introduction Python pika](https://www.rabbitmq.com/tutorials/tutorial-one-python.html)
- [Publisher Confirms and Consumer Acknowledgements](https://www.rabbitmq.com/confirms.html)
- [Production Checklist](https://www.rabbitmq.com/production-checklist.html)

