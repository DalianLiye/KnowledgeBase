# 关于DAG
DAG全称：Directed Acyclic Graph （向无环图）, 它是 Airflow的核心概念\
DAG包含了一组task的集合，DAG中定义了如何运行集合中的task，比如task的执行顺序，各task执行前后的依赖关系
不包含任何task的DAG毫无意义

DAG中包含的task包含以下种类：
- Operators
- Sensors
- TaskFlow

DAG里定义了DAG的执行频率，比如每5分钟，每天，每年的1月1日等
DAG仅仅是一个调度工具，它并不关心task的具体内容，只关心task的执行顺序，执行时间，执行次数，执行超时这样的操作


# 定义DAG
三种方式定义DAG
- **方式1：** 使用with语句(上下文管理器)将任何内容都隐式的加入到DAG中
```python
 import datetime
 from airflow import DAG
 from airflow.operators.empty import EmptyOperator

 with DAG(
     dag_id="my_dag_name",
     start_date=datetime.datetime(2021, 1, 1),
     schedule="@daily",
 ):
     EmptyOperator(task_id="task")
```

- **方式2：** 使用标准构造函数，将DAG传递给使用的任何运算符
```python
 import datetime
 from airflow import DAG
 from airflow.operators.empty import EmptyOperator

 my_dag = DAG(
     dag_id="my_dag_name",
     start_date=datetime.datetime(2021, 1, 1),
     schedule="@daily",
 )
 EmptyOperator(task_id="task", dag=my_dag)
```

- **方式3：** 使用 @dag 装饰器将函数转换为 DAG 生成器
```python
import datetime
from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator

@dag(start_date=datetime.datetime(2021, 1, 1), schedule="@daily")
def generate_dag():
    EmptyOperator(task_id="task")

generate_dag()
```

# Task依赖
DAG里通常不会只有一个task，它会定义多个task，而各task之间通常也是有依赖关系的

Task之间依赖关系的定义主要有以下两种方式：
- **方式1：** 使用操作符>>和<<(推荐)
```python
first_task >> [second_task, third_task]
third_task << fourth_task
```

- **方式2：** 使用set_upstream和set_downstream方法显式的指定task的上下游task
```python
first_task.set_downstream([second_task, third_task])
third_task.set_upstream(fourth_task)
```

- **方式3：** 使用cross_downstream定义两组task之间的上下游关系
```python
from airflow.models.baseoperator import cross_downstream

# Replaces
# [op1, op2] >> op3
# [op1, op2] >> op4
cross_downstream([op1, op2], [op3, op4])
```

- **方式4：** 使用chain函数将各单独的task进行线性连接
```python
from airflow.models.baseoperator import chain

# Replaces op1 >> op2 >> op3 >> op4
chain(op1, op2, op3, op4)

# You can also do it dynamically
chain(*[EmptyOperator(task_id='op' + i) for i in range(1, 6)])
```

- **方式5：** 使用chain函数将单独的task和一组task进行线性连接\
	**注：** 
	- 各task组的task数目必须是一致的
	- 该种方式跟cross_downstream是不一样的,cross_downstream是两个task组的task之间进行交叉连接,而chain是将两个task组的task之间进行对应位置的task进行连接
```python
from airflow.models.baseoperator import chain

# Replaces
# op1 >> op2 >> op4 >> op6
# op1 >> op3 >> op5 >> op6
chain(op1, [op2, op3], [op4, op5], op6)
```



# DAG加载
Airflow通过加载python源文件来加载DAG，这些python源文件被放置在配置属性DAG_FOLDER所指定的路径下
Airflow会获取DAG_FOLDER下的每个文件，执行它，然后从该文件中加载任何DAG对象
因此一个python文件可定义多个DAG，也一个DAG也可使用多个python文件(通过import方式整合)

Airflow从Python文件加载DAG时，它只会提取顶级的任何对象，这些对象是DAG实例

dag_1会被加载，dag_1定义在顶层(globals,即定义在全局域)
dag_2不会被加载，dag_1定义方法内部(local，即定义在局部)
```python
dag_1 = DAG('this_dag_will_be_discovered')

def my_function():
    dag_2 = DAG('but_this_dag_will_not')

my_function()
```

**注：**
Airflow在DAG_FOLDER中搜索DAG时，Airflow仅将包含字符串airflow和dag（不区分大小写）的Python文件作为优化项考虑在内
要考虑所有Python文件，请禁用 DAG_DISCOVERY_SAFE_MODE 配置标志

可以在DAG_FOLDER或其任何子文件夹中提供一个 .airflowignore 文件，该文件描述了加载器要忽略的文件模式
它涵盖了它所在的目录以及其下的所有子文件夹

当.airflowignore无法满足需求，并且希望以更灵活的方式控制Airflow是否需要解析Python文件时，可通过在配置文件中设置might_contain_dag_callable来插入可调用项
该可调用项将替换默认的Airflow启发式方法，即检查Python文件中是否存在字符串airflow和dag（不区分大小写）
```python
def might_contain_dag(file_path: str, zip_file: zipfile.ZipFile | None = None) -> bool:
    # Your logic to check if there are DAGs defined in the file_path
    # Return True if the file_path needs to be parsed, otherwise False
```



# DAG执行

通过以下方式执行DAG：
- 手动或API触发DAG（manual）
- 设置预定执行时间（schedule）

schedule不是DAG的必须项，但通常需要为DAG定义一个schedule
schedule是通过schedule参数设定
```python
with DAG("my_daily_dag", schedule="@daily"):
    ...
```

schedule参数值有以下几种
```pythn
with DAG("my_daily_dag", schedule="0 0 * * *"):
    ...

with DAG("my_one_time_dag", schedule="@once"):
    ...

with DAG("my_continuous_dag", schedule="@continuous"):
    ...
```

## DAG RUN
DAG每次的执行表示一个DAG RUN

同一个DAG的多个DAG RUN可以并行，每一个DAG RUN都有自己定义的数据间隔，用于标识DAG Task应操作的数据周期

比如有一个DAG每天都会处理当天的数据，此时DAG的内部逻辑发生改变，需要用新的逻辑重新处理过去三个月的数据
此种情况，可以通过回填DAG解决，即重新执行过去三个月里该DAG每天的DAG RUN
因为过去三个月里每天的DAG RUN都只处理其所在当天数据周期的数据，每天的DAG RUN之间不会相互影响，可以在同一时间点执行这些历史三个月里每天的DAG RUN

DAG每次的执行表示一个DAG RUN，DAG中task每次的执行表示一个task instance

DAG RUN有以下三个时间：
- **start date：** DAG RUN实际的启动时间
- **end date：** DAG RUN实际的结束时间
- **logical date（正式称为execution date）：** DAG RUN计划或触发的预期时间，之所以将其称为logical date，是因为它具有抽象的本质，具有多种含义，具体取决于 DAG 运行本身的上下文

当DAG RUN是手动触发，则其logical date将为触发DAG RUN的日期和时间，并且该值应等于DAG RUN的start date
当DAG RUN是被按照预定时间自动调度触发，并设置了特定的调度间隔，则其logical date将指示它标记数据间隔开始的时间，其中DAG RUN的start date将是logical date + 调度间隔









# DAG自动暂停
DAG可以被设置为自动暂停
以下属性可以让DAG在连续N次执行失败后，自动暂停
- max_consecutive_failed_dag_runs_per_dag

可以在DAG里通过以下属性，覆盖掉上面的属性值
- max_consecutive_failed_dag_runs

注：该属性在2.9.3版本尚属于实验阶段，不稳定
