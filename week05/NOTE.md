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
    Brocker	：消息队列服务器实体
    Exchange	：消息交换机，指定消息按什么规则，路由到哪个队列。 默认的 exchange 是direct；
    Queue	：消息队列，每个消息都会被投入到一个或者多个队列里。
    Binding	：绑定，它的作用是把exchange和queue按照路由规则binding起来。
    Routing Key	：路由关键字，exchange根据这个关键字进行消息投递。
    Vhost	：虚拟主机，一个broker里可以开设多个vhost，用作不用用户的权限分离。
    Producer	：消息生产者，就是投递消息的程序。
    Consumer	：消息消费者，就是接受消息的程序。
    Channel	：消息通道，在客户端的每个连接里，可建立多个channel，每个channel代表一个会话任务。
```

2. Python pika
- [Introduction Python pika](https://www.rabbitmq.com/tutorials/tutorial-one-python.html)
- [Publisher Confirms and Consumer Acknowledgements](https://www.rabbitmq.com/confirms.html)
- [Production Checklist](https://www.rabbitmq.com/production-checklist.html)



<br/>

## 作业三：请用自己的语言描述如下问题：

#### 1. 在你目前的工作场景中，哪个业务适合使用 rabbitmq？ 引入 rabbitmq 主要解决什么问题?（非相关工作可以以设计淘宝购物和结账功能为例来描述）
-    异步下单：用户下单后，订单系统完成持久化处理，将消息写入消息队列，返回用户订单下单成功。库存系统根据下单信息，进行库存操作。假如：库存系统有问题，也不影响正常下单；  
-    流量削峰：秒杀活动中，使用消息队列隔离 前端的网关和后端服务，只要网关在处理 APP 请求时增加一个获取令牌的逻辑；   获取到令牌则继续调用后端秒杀服务，如果获取不到令牌则直接返回秒杀失败。
-    服务解耦：订单服务在订单变化时发送一条消息到消息队列的一个主题 Order 中，所有下游系统都订阅主题 Order，这样每个下游系统都可以获得一份实时完整的订单数据。

#### 2. 如何避免消息重复投递或重复消费？
-   用幂等性解决重复消息问题；一个幂等操作的特点是，其任意多次执行所产生的影响均与一次执行的影响相同。
   
#### 3. 交换机 fanout、direct、topic 有什么区别？

```
  fanout	: 不处理路由键，所有bind到此Exchange 的queue都可以接收消息
  direct	: 通过routingKey和exchange决定的那个唯一的queue可以接收消息
  topic 	: 所有符合routingKey(此时可以是一个表达式)的routingKey所bind的queue可以接收消息
```

#### 4. 架构中引入消息队列是否利大于弊？你认为消息队列有哪些缺点？
 - 缺点：架构复杂，学习成本高； 同时对中间件的性能、稳定性是个考验；   
 - 有点：异步处理、流量控制、服务解耦  
