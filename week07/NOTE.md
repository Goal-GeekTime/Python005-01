学习笔记

### 作业一：区分以下类型哪些是容器序列哪些是扁平序列，哪些是可变序列哪些是不可变序列：
> - 可变数据类型：
> 1. 列表 list
> 1. 字典 dict
> 1. 双向队列对象 collections.deque

<br/>

> - 不可变数据类型：
> 1. 整型 int
> 1. 浮点型 float
> 1. 字符串型 string
> 1. 元组 tuple

<br/>

> - 序列分类
> 1. 容器序列：list、tuple、collections.deque 等，能存放不同类型的数据 容器序列可以存放不同类型的数据。
> 1. 扁平序列：str、bytes、bytearray、memoryview (内存视图)、array.array 等，存放的是相同类型的数据 扁平序列只能容纳一种类型。


<br/>

### 作业二：自定义一个 python 函数，实现 map() 函数的功能。
homework_2/my_map.py


<br/>

### 作业三：实现一个 @timer 装饰器，记录函数的运行时间，注意需要考虑函数可能会接收不定长参数。
homework_3/timer.py