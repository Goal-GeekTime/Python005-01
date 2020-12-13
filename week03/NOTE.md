学习笔记


## 1. 在 Linux 环境下，安装 MySQL5.6 以上版本，修改字符集为 UTF8mb4 并验证，新建一个数据库 testdb，并为该数据库增加远程访问的用。

1. 安装
    ```
    # rpm -ivh https://dev.mysql.com/get/mysql80-community-release-el7-3.noarch.rpm
    # rpm -ivh https://dev.mysql.com/get/mysql80-community-release-el7-3.noarch.rpm
    # yum repolist all | grep mysql

    # yum-config-manager --disable mysql80-community
    # yum-config-manager --enable mysql57-community

    # yum install -y mysql-community-server
    ```

2. 修改字符集
    ```
    # vim /etc/my.cnf
        [client]
        default_character_set = utf8mb4

        [mysqld]
        default_character_set = utf8mb4
        # 服务器为每个链接客户端执行的字符串
        init_connect = 'SET NAMES utf8mb4'
        # 控制客户端连接握手时候不使用默认的校对规则。使用 collation_server 规定的校对规则。
        character_set_client_handshake = FALSE
        # 设置排序规则。unicode 表示区分大小写，ci 表示大小写不敏感。cs 表示大小写敏感
        collation_server = utf8mb4_unicode_ci
    ```

3. 启动、初始化用户登录、授权
    ```
    # systemctl start mysqld.service
    # systemctl enable mysqld.service

    # grep 'temporary password' /var/log/mysqld.log
    # mysql -uroot -p

    mysql> set global validate_password_policy=0;       # 如果需要更改密码策略

    mysql> ALTER USER 'root'@'%' IDENTIFIED BY 'bridge!';
    mysql> select user,host,authentication_string from mysql.user;


    mysql> SHOW VARIABLES LIKE '%character%';           # 查看字符集
    ```




## 2. 使用 sqlalchemy ORM 方式创建如下表，使用 PyMySQL 对该表写入 3 条测试数据，并读取:
1. 创建表和导入测试数据
   $ cd homework_2
   $ python orm_learn.py

2. 创建表  & 插入、查找
    ```
    class UserTable(Base):
        """
        # 用户 id、用户名、年龄、生日、性别、学历、字段创建时间、字段更新时间
        """
        __tablename__ = 'user'
        uid = Column(BigInteger(), primary_key=True)
        name = Column(String(50), nullable=False)
        age = Column(Integer())
        birthday = Column(Date())
        gender = Column(CHAR(10))
        education = Column(String(50))
        create_time = Column(TIMESTAMP(3), default=get_time())
        update_time = Column(TIMESTAMP(3), onupdate=get_time(), default=get_time())
    ```

    ```
    # 插入
    Session_class = sessionmaker(bind=engine)
    Session = Session_class()  
    user1 = UserTable(name=name, age=age, birthday=birthday, gender=gender, education=education)
    user2 = UserTable(name=name, age=age, birthday=birthday, gender=gender, education=education)
    session.add(user1)
    session.add(user2)
    Session.commit() 

    # 查询
    for result in Session.query(UserTable):
        print(result)

    # 统计分组查询
    query = session.query(UserTable.education, func.count(UserTable.education)).group_by(UserTable.education)
    query = query.order_by(desc(func.count(UserTable.education)))
    ```



## 3. 为以下 sql 语句标注执行顺序：
    ```
    SELECT DISTINCT player_id, player_name, count(*) as num     # 步骤5      
    FROM player JOIN team ON player.team_id = team.team_id      # 步骤1
    WHERE height > 1.80                                         # 步骤2
    GROUP BY player.team_id                                     # 步骤3
    HAVING num > 2                                              # 步骤4
    ORDER BY num DESC                                           # 步骤6
    LIMIT 2                                                     # 步骤7
    ```




## 4. 以下两张基于 id 列，分别使用 INNER JOIN、LEFT JOIN、 RIGHT JOIN 的结果是什么?

1. 创建表、插入数据等
    ```
    mysql>  CREATE TABLE IF NOT EXISTS `t1` (
                `id` int(11) NOT NULL AUTO_INCREMENT, 
                `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
                PRIMARY KEY (`id`) USING BTREE
            )ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

    mysql> CREATE  TABLE t2 LIKE t1;

    mysql> INSERT INTO t1(name) VALUES('t1_小李'),('t1_小刘'),('t1_六');
    mysql> INSERT INTO t2(id,name) VALUES(1,'t2_小王'),(2,'t2_小娲'),(10,'t2_小碗');


    mysql> select * from t1;
    +----+-----------+
    | id | name      |
    +----+-----------+
    |  1 | t1_小李   |
    |  2 | t1_小刘   |
    |  3 | t1_六     |
    +----+-----------+
    3 rows in set (0.00 sec)

    mysql> select * from t2;
    +----+-----------+
    | id | name      |
    +----+-----------+
    |  1 | t2_小王   |
    |  2 | t2_小娲   |
    | 10 | t2_小碗   |
    +----+-----------+
    3 rows in set (0.00 sec)
    ``` 


2. INNER JOIN
    ```
    mysql> SELECT t1.id, t1.name, t2.id, t2.name 
    FROM t1 
    INNER JOIN t2
    ON t1.id = t2.id
    +----+-----------+----+-----------+
    | id | name      | id | name      |
    +----+-----------+----+-----------+
    |  1 | t1_小李   |  1 | t2_小王   |
    |  2 | t1_小刘   |  2 | t2_小娲   |
    +----+-----------+----+-----------+
    2 rows in set (0.00 sec)
    ```



3. LEFT JOIN
    ```
    mysql> SELECT t1.id, t1.name, t2.id, t2.name 
    FROM t1 
    LEFT  JOIN t2
    ON t1.id = t2.id;
    +----+-----------+------+-----------+
    | id | name      | id   | name      |
    +----+-----------+------+-----------+
    |  1 | t1_小李   |    1 | t2_小王   |
    |  2 | t1_小刘   |    2 | t2_小娲   |
    |  3 | t1_六     | NULL | NULL      |
    +----+-----------+------+-----------+
    3 rows in set (0.00 sec)
    ```



4. RIGHT JOIN
    ```
    mysql> SELECT t1.id, t1.name, t2.id, t2.name 
    FROM t1 
    RIGHT  JOIN t2
    ON t1.id = t2.id
    +------+-----------+----+-----------+
    | id   | name      | id | name      |
    +------+-----------+----+-----------+
    |    1 | t1_小李   |  1 | t2_小王   |
    |    2 | t1_小刘   |  2 | t2_小娲   |
    | NULL | NULL      | 10 | t2_小碗   |
    +------+-----------+----+-----------+
    3 rows in set (0.00 sec)
    ```




## 5. 使用 MySQL 官方文档，学习通过 sql 语句为上题中的 id 和 name 增加索引，并验证。根据执行时间，增加索引以后是否查询速度会增加？请论述原因，并思考什么样的场景下增加索引才有效。
1. 创建表和导入测试数据
   $ cd homework_5
   $ python index.py

2. 普通索引的创建
    ```
    1. create index indexname on mytable(username(length));  
    2. alter table tablename add index indexname(columnname1,columnname2)
    3. create table mytable(
        id int not null,
        username varchar(16) not null,
        index [indexName] (username(length))     # indexName可以省略，默认按列名字命名索引名
    );
    ```

3. 有无索引区别 
    ```
    mysql> explain select * from user_has_index where  name = 'Abejundio_a';
    +----+-------------+----------------+------------+------+---------------+------+---------+-------+------+----------+-------------+
    | id | select_type | table          | partitions | type | possible_keys | key  | key_len | ref   | rows | filtered | Extra       |
    +----+-------------+----------------+------------+------+---------------+------+---------+-------+------+----------+-------------+
    |  1 | SIMPLE      | user_has_index | NULL       | ref  | name          | name | 202     | const |  134 |   100.00 | Using index |
    +----+-------------+----------------+------------+------+---------------+------+---------+-------+------+----------+-------------+
    1 row in set, 1 warning (0.00 sec)


    mysql> explain select * from user_no_index where  name = 'Abejundio_a';
    +----+-------------+---------------+------------+------+---------------+------+---------+------+-------+----------+-------------+
    | id | select_type | table         | partitions | type | possible_keys | key  | key_len | ref  | rows  | filtered | Extra       |
    +----+-------------+---------------+------------+------+---------------+------+---------+------+-------+----------+-------------+
    |  1 | SIMPLE      | user_no_index | NULL       | ALL  | NULL          | NULL | NULL    | NULL | 29715 |    10.00 | Using where |
    +----+-------------+---------------+------------+------+---------------+------+---------+------+-------+----------+-------------+
    1 row in set, 1 warning (0.00 sec)
    ```

    得出结论：
    1. 有索引，并且仅查询 index(name) 字段， Using index  表示使用了覆盖索引 (覆盖了 select 的字段，不需要回表)； 并且 Rows 估算只需读取记录行数为 134行；
    2. 无索引，使用 where 条件查找， Rows 估算为全表扫描；

4.  官方文档
    [MySQL 8.0 Reference Manual](https://dev.mysql.com/doc/refman/8.0/en/mysql-indexes.html)
    [CREATE INDEX语句](https://dev.mysql.com/doc/refman/8.0/en/create-index.html)



##  6. 张三给李四通过网银转账 100 极客币，现有数据库中三张表：

一张为用户表，包含用户 ID 和用户名字，另一张为用户资产表，包含用户 ID 用户总资产，
第三张表为审计用表，记录了转账时间，转账 id，被转账 id，转账金额。

请合理设计三张表的字段类型和表结构；
请实现转账 100 极客币的 SQL(可以使用 pymysql 或 sqlalchemy-orm 实现)，张三余额不足，转账过程中数据库 crash 等情况需保证数据一致性。

1. 创建表和导入测试数据
   $ cd homework_6
   $ python orm_three_table.py

    ```
    class UserTable(Base):
        """
        # 用户表: id、用户名
        """
        __tablename__ = 'account'
        uid = Column(BigInteger(), primary_key=True)
        name = Column(String(50), nullable=False)

    class UserAsset(Base):
        """
        # 资产表: id、用户id、总资产
        """
        __tablename__ = 'asset'
        id = Column(BigInteger(), primary_key=True)
        uid = Column(Integer,ForeignKey("account.id")) 
        total_asset = Column(BigInteger()

     class UserAsset(Base):
        """
        # 审计表: id、转账 id，被转账 id，转账金额、字段创建时间
        """
        __tablename__ = 'audit'
        id = Column(BigInteger(), primary_key=True)
        tran_id = Column(Integer,ForeignKey("account.id") ,comment='转账id') 
        des_id = Column(Integer,ForeignKey("account.id") ,comment='被转账转账id') 
        create_time = Column(TIMESTAMP(3), default=get_time())
