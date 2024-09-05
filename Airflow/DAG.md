# 关于DAG
DAG全称：Directed Acyclic Graph （向无环图）, 它是 Airflow的核心概念\
DAG包含了一组task的集合，DAG中定义了如何运行集合中的task，比如各task之间的执行顺序，以及执行前后的依赖关系\
一个DAG如果不包含任何task将毫无意义

DAG中的task包含以下种类：
- Operators
- Sensors
- TaskFlow

DAG里定义了DAG的执行频率，比如每5分钟，每天，每年的1月1日等\
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

- **方式2：** 使用标准构造函数，将DAG传递给使用的任何operator/task
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

- **方式3：** 使用@dag装饰器将函数转换为DAG生成器
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
DAG里通常会定义多个task，而各task之间通常也是有依赖关系的

Task之间依赖关系的定义主要有以下两种方式：
- **方式1：** 使用操作符>>和<<(推荐)
```python
first_task >> [second_task, third_task]
third_task << fourth_task
```

- **方式2：** 使用set_upstream和set_downstream函数显式的指定task的上下游
```python
first_task.set_downstream([second_task, third_task])
third_task.set_upstream(fourth_task)
```

- **方式3：** 使用cross_downstream函数定义两组task之间的上下游关系（交叉依赖）
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



# 加载DAG
Airflow通过加载python源文件来加载DAG，这些python源文件被放置在配置属性DAG_FOLDER所指定的路径下\
Airflow会获取DAG_FOLDER下的每个文件后并执行它，然后从该文件中加载所有DAG对象\
因此一个python文件可定义多个DAG，也一个DAG也可使用多个python文件(通过import方式整合)

Airflow从Python文件加载DAG时，它只会提取顶级（global域）的任何DAG对象(DAG实例)

**示例:**\
dag_1会被加载，dag_1定义在顶层(globals,即定义在全局域)\
dag_2不会被加载，dag_1定义方法内部(local，即定义在局部)
```python
dag_1 = DAG('this_dag_will_be_discovered')

def my_function():
    dag_2 = DAG('but_this_dag_will_not')

my_function()
```

**注：**\
Airflow在DAG_FOLDER中搜索DAG时，Airflow仅将包含字符串airflow和dag（不区分大小写）的Python文件作为优化项考虑在内\
要考虑所有Python文件，请禁用DAG_DISCOVERY_SAFE_MODE配置标志

可以在DAG_FOLDER或其任何子文件夹中提供一个 .airflowignore文件，该文件描述了加载器要忽略的文件模式，它涵盖了它所在的目录以及其所有子文件夹

当.airflowignore无法满足需求，并且希望以更灵活的方式控制Airflow是否需要解析Python文件时，可通过在配置文件中设置might_contain_dag_callable来插入可调用项\
该可调用项将替换默认的Airflow启发式方法，即检查Python文件中是否存在字符串airflow和dag（不区分大小写）
```python
def might_contain_dag(file_path: str, zip_file: zipfile.ZipFile | None = None) -> bool:
    # Your logic to check if there are DAGs defined in the file_path
    # Return True if the file_path needs to be parsed, otherwise False
```



# 运行DAG
通过以下方式执行DAG：
- 手动或API触发DAG（manual）
- 设置预定执行时间（schedule）

设置DAG的预定执行时间不是必须的，但通常需要为DAG定义\
预定执行时间是通过schedule参数设定
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
DAG每次的执行表示一个DAG RUN\
同一个DAG的多个DAG RUN可以并行执行，每一个DAG RUN都有自己定义的数据间隔，用于标识DAG RUN里task应操作的数据周期

比如有一个DAG每天都会处理上游在当天的数据，此时DAG的内部逻辑发生改变，需要用新的逻辑重新处理过去三个月的数据\
此种情况，可以通过回填DAG解决，即重新执行该DAG在过去三个月里的每一天的DAG RUN\
因为过去三个月里每一天的DAG RUN都只处理其所在当天数据周期的数据，每天的DAG RUN之间不会相互影响，因此可以在同一时间点执行这些历史三个月里每天的DAG RUN

DAG每次的执行表示一个DAG RUN，DAG中task每次的执行表示一个task instance

DAG RUN有以下三个时间：
- **start date：** DAG RUN实际的启动时间
- **end date：** DAG RUN实际的结束时间
- **logical date（正式称为execution date）：** DAG RUN计划或触发的预期时间，之所以将其称为logical date，是因为它具有抽象的本质，具有多种含义，具体取决于 DAG 运行本身的上下文

当DAG RUN是手动触发，则其logical date将为触发DAG RUN的日期和时间，并且该值应等于DAG RUN的start date\
当DAG RUN是被按照预定时间自动调度触发，并设置了特定的调度间隔，则其logical date将指示它标记数据间隔开始的时间，其中DAG RUN的start date将是logical date + 调度间隔




# DAG分配
一个Operator/Task如果要被执行，必须先为其指定一个DAG\
以下方式可以隐式的指定DAG:
- 在with DAG块中声明Operator/Task
- 在@dag装饰器中声明Operator/Task
- 将Operator/Task指定为已经分配了DAG的Operator/Task的上游或下游

以上方式除外，则必须使用dag=为Operator/Task指定DAG


# 默认参数
通常，DAG中的许多Operator/Task需要相同的默认参数集（比如retries）\
与其为每个Operator/Task单独指定此项，不如在创建DAG时将default_args传递给DAG，它将自动将它们应用于与之绑定的任何Operator/Task
```python
import pendulum

with DAG(
    dag_id="my_dag",
    start_date=pendulum.datetime(2016, 1, 1),
    schedule="@daily",
    default_args={"retries": 2},
):
    op = BashOperator(task_id="hello_world", bash_command="Hello World!")
    print(op.retries)  # 2
```


# DAG装饰器
2.0版中的新增功能\
除了使用with上下文管理器或DAG()构造函数声明单个DAG的传统方法之外，还可以使用@dag装饰函数，将其转换为DAG生成器函数
```python
@dag(
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["example"],
)
def example_dag_decorator(email: str = "example@example.com"):
    """
    DAG to send server IP to email.

    :param email: Email to send IP to. Defaults to example@example.com.
    """
    get_ip = GetRequestOperator(task_id="get_ip", url="http://httpbin.org/get")

    @task(multiple_outputs=True)
    def prepare_email(raw_json: dict[str, Any]) -> dict[str, str]:
        external_ip = raw_json["origin"]
        return {
            "subject": f"Server connected from {external_ip}",
            "body": f"Seems like today your server executing Airflow is connected from IP {external_ip}<br>",
        }

    email_info = prepare_email(get_ip.output)

    EmailOperator(
        task_id="send_email", to=email, subject=email_info["subject"], html_content=email_info["body"]
    )


example_dag = example_dag_decorator()
```
除了作为一种创建DAG的新方法之外，该装饰器还会将函数中的任何参数设置为DAG参数，在触发DAG时设置这些参数\
然后就可以从Python代码或{{ context.params }}中访问这些参数，这些代码位于Jinja模板中

注：Airflow仅加载出现在DAG文件顶层的DAG，这意味着不能仅仅使用@dag声明一个函数，还必须在DAG文件中至少调用它一次，并将其分配给顶层对象


# 控制流(Control Flow)
默认情况下，DAG中的一个task仅在其所有依赖的task都成功才运行，但是有几种方法可以修改此设置

- **Branching(分支):** 根据条件选择要继续执行的任务
- **Trigger Rules(触发规则)：** 设置 DAG 运行任务的条件
- **Setup and Teardown(设置和拆除)：** 定义设置和拆除关系
- **Latest Only(仅最新)：** 一种特殊形式的分支，仅在针对当前运行的 DAG 运行
- **Depends On Past(依赖过去)：** 任务可以依赖于自己从之前的运行



## branching（分支）
利用branching（分支）可以让DAG在执行task时，根据需要有选择的执行一个或多个路径的下游task

分支通过@task.branch装饰器实现

@task.branch装饰器与@task非常相似，不同之处在于它期望装饰的函数返回一个task ID（或 task ID列表）\
然后将只执行返回的task ID或task ID列表所对应的下游task及其对应路径，其他路径都将被跳过\
它还可以返回 None以跳过所有下游任务

Python 函数返回的 task_id 必须引用 @task.branch 装饰的任务直接下游的一个任务

当一个任务既是分支操作符的下游，又是所选任务之一或多个的下游时，它将不会被跳过

**示例：** 
@task.branch 还可以与XCom一起使用，允许分支上下文根据上游task动态决定要遵循哪个分支
```python
@task.branch(task_id="branch_task")
def branch_func(ti=None):
    xcom_value = int(ti.xcom_pull(task_ids="start_task"))
    if xcom_value >= 5:
        return "continue_task"
    elif xcom_value >= 3:
        return "stop_task"
    else:
        return None


start_op = BashOperator(
    task_id="start_task",
    bash_command="echo 5",
    do_xcom_push=True,
    dag=dag,
)

branch_op = branch_func()

continue_op = EmptyOperator(task_id="continue_task", dag=dag)
stop_op = EmptyOperator(task_id="stop_task", dag=dag)

start_op >> branch_op >> [continue_op, stop_op]
```


如果希望使用分支功能实现自己的运算符，则可以从BaseBranchOperator继承，它的行为类似于@task.branch装饰器，但要求提供方法choose_branch的实现

**注：**
@task.branch装饰器比在DAG中直接实例化BranchPythonOperator更为推荐\
后者通常只应被子类化以实现自定义运算符

**示例：**
与@task.branch的可调用对象一样，此方法可以返回下游task ID或task ID列表\
这些返回task ID或task ID列表所对应的下游task将被运行，而所有其他任务都将被跳过\
它还可以返回None以跳过所有下游任务
```python
class MyBranchOperator(BaseBranchOperator):
    def choose_branch(self, context):
        """
        Run an extra branch on the first day of the month
        """
        if context['data_interval_start'].day == 1:
            return ['daily_task_id', 'monthly_task_id']
        elif context['data_interval_start'].day == 2:
            return 'daily_task_id'
        else:
            return None
```

类似于常规Python代码的@task.branch 装饰器，还有一些分支装饰器，它们使用名为 @task.branch_virtualenv 的虚拟环境或名为 @task.branch_external_python 的外部 python
















## Latest Only
DAG RUN通常针对的日期与当前日期不同， 例如，为上个月的每一天运行一个 DAG 副本以回填一些数据\
当不希望让DAG的某些（或全部）部分针对以前日期运行，可以使用LatestOnlyOperator

比如当执行历史某一个DAG RUN时，不希望taskA，taskB，taskC被执行，可以将一个LatestOnlyOperator设置为taskA，taskB，taskC的直接上游(使用默认trigger rule)
这样在执行历史DAG RUN时taskA，taskB，taskC就不会被执行\
只有执行最新的DAG RUN时（当前时间介于其execution_time和下一个计划的execution_time之间，并且它不是外部触发的运行）taskA，taskB，taskC才会被执行

```python
import datetime

import pendulum

from airflow.models.dag import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.latest_only import LatestOnlyOperator
from airflow.utils.trigger_rule import TriggerRule

with DAG(
    dag_id="latest_only_with_trigger",
    schedule=datetime.timedelta(hours=4),
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["example3"],
) as dag:
    latest_only = LatestOnlyOperator(task_id="latest_only")
    task1 = EmptyOperator(task_id="task1")
    task2 = EmptyOperator(task_id="task2")
    task3 = EmptyOperator(task_id="task3")
    task4 = EmptyOperator(task_id="task4", trigger_rule=TriggerRule.ALL_DONE)

    latest_only >> task1 >> [task3, task4]
    task2 >> [task3, task4]
```
task1是latest_only的直接下游，并且除了最新版本之外，所有运行都将跳过它\
task2完全独立于latest_only，并且将在所有计划周期中运行\
task3是task1和task2的下游，并且由于默认 触发规则为all_success，因此将从task1接收级联跳过\
task4是task1和task2的下游，但它不会被跳过，因为它的trigger_rule设置为all_done\




## Depends On Past
只有当上一个DAG RUN中的该task的task instance成功运行后，该task才能运行
**示例：**
```python
task01 = EmptyOperator(task_id="task01", depends_on_past=true,dag=dag)
```

**注:**
如果在DAG生命周期的开始阶段运行DAG（DAG第一次运行，没有历史执行记录），则task仍将运行，因为没有上一个DAG RUN可依赖



## Trigger Rules(触发规则)
默认情况下，一个task会等待其所有直接上游task成功之后才运行，可以使用trigger_rule参数修改此种默认方式

trigger_rule有以下选项：
- **all_success（默认）：** 所有上游task都已成功
- **all_failed：** 所有上游task都处于failed或upstream_failed状态
- **all_done：** 所有上游task都已完成执行
- **all_skipped：** 所有上游task都处于skipped状态
- **one_failed：** 至少有一个上游task失败（不等待所有上游task完成）
- **one_success：** 至少有一个上游task成功（不等待所有上游task完成）
- **one_done：** 至少有一个上游task成功或失败
- **none_failed：** 所有上游task均未failed 或upstream_failed，即所有上游task均已成功或已跳过
- **none_failed_min_one_success：** 所有上游task均未failed或upstream_failed，且至少有一个上游task已成功
- **none_skipped：** 没有上游task处于已跳过状态，即所有上游task均处于success、failed或upstream_failed状态
- **always：** 没有任何依赖项，随时运行此task


还可以将其与Depends On Past功能结合使用

**注：**\
了解Trigger Rules与skipped tasks之间的交互非常重要，尤其是作为分支操作的一部分而被跳过的task\
分支操作的所有下游分支task一般不会使用all_success或all_failed\
因为既然是分支，那么只能有一个或多个分支会往下走，剩下的分支就是skipped，如果下游都是all_success或all_failed，那么就都skipped了

**示例：**
skipped tasks将通过触发规则all_success和all_failed级联，并导致它们也被跳过
```python
# dags/branch_without_trigger.py
import pendulum

from airflow.decorators import task
from airflow.models import DAG
from airflow.operators.empty import EmptyOperator

dag = DAG(
    dag_id="branch_without_trigger",
    schedule="@once",
    start_date=pendulum.datetime(2019, 2, 28, tz="UTC"),
)

run_this_first = EmptyOperator(task_id="run_this_first", dag=dag)


@task.branch(task_id="branching")
def do_branching():
    return "branch_a"


branching = do_branching()

branch_a = EmptyOperator(task_id="branch_a", dag=dag)
follow_branch_a = EmptyOperator(task_id="follow_branch_a", dag=dag)

branch_false = EmptyOperator(task_id="branch_false", dag=dag)

#join task将显示为已跳过
#因为其trigger_rule默认设置为all_success，并且由分支操作导致的跳过会级联跳过标记为all_success的任务
join = EmptyOperator(task_id="join", dag=dag) 

#通过在join task中将trigger_rule设置为none_failed_min_one_success，可以将join task显式为success
join = EmptyOperator(task_id="join", trigger_rule='none_failed_min_one_success',dag=dag) 

run_this_first >> branching
branching >> branch_a >> follow_branch_a >> join
branching >> branch_false >> join
```


## 设置和拆除
在数据工作流中，通常会创建资源（例如计算资源），使用它来完成一些工作，然后将其拆除\
Airflow提供设置和拆除task来支持此需求



# DAG自动暂停
DAG可以被设置为自动暂停\
以下属性可以让DAG在连续N次执行失败后，自动暂停
- max_consecutive_failed_dag_runs_per_dag

可以在DAG里通过以下属性，覆盖掉上面的属性值
- max_consecutive_failed_dag_runs

注：该属性在2.9.3版本尚属于实验阶段，不稳定
