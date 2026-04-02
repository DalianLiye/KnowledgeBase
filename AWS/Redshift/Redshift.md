# Table设计

## 关于各自段类型的选择

- 整型（INTEGER、SMALLINT、BIGINT）	
  适用于存储不小于零的整数值。选择具体的整型大小时应考虑数据的范围	
  例如：id，batch_num

- 浮点型（FLOAT、DOUBLE PRECISION）	
  用于存储需要小数点的数值，适合科学计算或需要高精度的财务数据	
  例如：金额相关

- 字符型（CHAR、VARCHAR）	
  存储字符串数据。CHAR 适用于固定长度字符串，VARCHAR 适用于可变长度字符串	value包含字符
  例如：description, name

- 时间和日期型（DATE、TIMESTAMP）	
  用于存储日期和时间数据。DATE 仅包含日期，TIMESTAMP 包含日期和时间	
  例如：update_time

- 布尔型（BOOLEAN）	
  存储真/假值	
  例如：用户是否激活、订单是否完成

  - 说明
  - 优点
  - 缺点
  - 使用场景

## 分配键
- KEY	
  - 说明
    根据指定的分布键进行分布，相同键值的数据行存储在同一个节点上
    ```sql
    CREATE TABLE example_table (
        column1 INT,
        column2 INT,
        column3 VARCHAR(100),
        ...
    )
    DISTSTYLE KEY
    DISTKEY (column1);
    ```
  - 优点
    1) 当分布键被正确选择时，能显著提高联接查询性能，减少数据移动。
    2) 利于大规模联接操作，在同一节点上进行查询加速
  - 缺点
    分布键选择不当可能导致数据倾斜，某个节点负载过重	
  - 使用场景
    频繁联接的表

- EVEN	
  - 说明
    将表中的数据均匀地分布在所有节点上
    ```sql
    CREATE TABLE example_table (
        column1 INT,
        column2 INT,
        column3 VARCHAR(100),
        ...
    )
    DISTSTYLE EVEN;
    ```
  - 优点
    1) 均匀分布数据以优化查询性能，避免单个节点成为瓶颈
    2) 有效利用存储空间
  - 缺点
    如果查询涉及多个表联接，可能会引发数据重新分配，导致一定的开销
  - 使用场景
    不频繁联接的表
	
- All
  - 说明
    将表中的所有数据复制到每个节点上
    ```sql
    CREATE TABLE example_table (
        column1 INT,
        column2 INT,
        column3 VARCHAR(100),
        ...
    )
    DISTSTYLE ALL;
    ```
  - 优点
    1) 消除重新分配的成本，减少数据传输
    2) 提高查询性能，因为每个节点有完整的数据可用
    3) 避免了数据在节点间的移动，简化了查询逻辑
  - 缺点
    1) 需要以集群中节点数量为倍数的存储空间
    2) 需要更多的时间来加载、更新或插入数据到该表在多个节点存储
  - 使用场景	
    1) 更新不频繁、不广泛的表
    2) 频繁联接的参考表，比如配置表

- AUTO	
  - 说明
    Redshift自动选择最佳的分布策略，通常基于表的大小和查询模式
    ```sql
    CREATE TABLE example_table (
        column1 INT,
        column2 INT,
        column3 VARCHAR(100),
        ...
    )
    DISTSTYLE AUTO;
    ```
  - 优点
    1) 减少配置和调优的复杂性
    2) 系统会动态调整分布策略以优化查询性能
  - 缺点
    自动选择未必总是最优的分布策略，特别是在使用情况发生变化时
  - 使用场景
    初学者或不确定最佳分布策略的用户
官方文档： https://docs.aws.amazon.com/zh_cn/redshift/latest/dg/t_Distributing_data.html


## 排序键

- 复合排序
  - 说明
    复合排序使用一个关键字段集，以特定的顺序进行排序。查询首先按第一个字段排序，如果第一个字段中有相同的值，则按第二个字段排序，以此类推
    ```sql
    CREATE TABLE example_table (
        column1 INT,
        column2 INT,
        column3 VARCHAR(100),
        ...
    )
    COMPOUND SORTKEY (column1, column2, column3);
    ```
  - 优点
    当查询的筛选条件应用了使用排序键前缀的条件（如筛选条件和联接）时，复合排序键最为有用，查询效率最高
    注：当查询只依赖于辅助排序列而不引用主列时，复合排序的性能优势会下降
  - 缺点
    对查询顺序的依赖使其适应性较差。如果查询不按排序键的第一个字段或者字段集的顺序进行过滤，性能优化效果显著下降
  - 使用场景	
    当查询模式及其顺序是相对稳定和可预测的情况下

- 交错排序	
  - 说明
    交错排序使用多个字段进行排序，每个字段在排序时享有相同的优先级。查询可以均衡地利用所有指定的排序键字段
    ```sql
    CREATE TABLE example_table (
        column1 INT,
        column2 INT,
        column3 VARCHAR(100),
        ...
    )
    INTERLEAVED SORTKEY (column1, column2, column3);
    ```
  - 优点
    对于多种查询模式，其性能表现较均衡
  - 缺点
    1) 由于数据需要同时按多个字段进行排序，插入操作会较慢，批量加载的效率也会受到影响。
    2) 使用交错排序的表不能被加入data share
  - 使用场景
    当查询模式及其顺序是灵活多变和不可预测的情况下
 官方文档：https://docs.aws.amazon.com/zh_cn/redshift/latest/dg/t_Sorting_data.html