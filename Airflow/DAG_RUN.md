# 关于DAG RUN
DAG RUN是一个对象，它表示DAG在某一个时间的一个实例\
只要执行DAG，就会创建一个DAG RUN，DAG中的task就会被执行\
DAG RUN的状态取决于DAG中task的执行状态\
每个DAG RUN彼此独立运行，因此可以同时运行多个DAG RUN


# DAG RUN状态
DAG RUN的最终状态取决于DAG执行完成后的结果\
DAG的执行取决于其所包含的task及task间的依赖\
当所有task都处于终端状态之一（即不能转换到其他状态，例如 success、failed 或 skipped）时，将向DAG RUN分配状态\
DAG RUN的状态分配基于所谓的"叶节点"或简称"叶"(终节点)，叶节点是没有子节点的任务

DAG运行有以下可能的终端状态
- **success：** 如果所有叶节点状态都是success或skipped
- **failed：** 如果任何叶节点状态都是failed或upstream_failed

**注：**\
如果某些task定义了一些特定的trigger rule，这些可能会导致一些意外的行为\
例如，如果有一个leaf task的触发规则为"all_done"，不管其他task的状态如何(比如failed),它都将执行\
如果它执行成功，那么整个DAG运行也将标记为success，即使会有task出现failed

在 Airflow 2.7 中添加
当一个DAG的最新的DAG RUN正在执行时，可以在"running"选项卡中找到\
当一个DAG的最新的DAG RUN被标记为failed，可以在"failed"选项卡中找到

# 数据间隔(Data Interval)
Airflow中的每个DAG RUN都有一个分配的"数据间隔"，表示其操作的时间范围\
例如，schedule是@daily的DAG，其每个数据间隔都将在每天午夜(00:00)开始，并在午夜(24:00)结束

DAG RUN通常在关联的数据间隔结束后启动，以确保DAG RUN能够收集该时间段内的所有数据\
也就是说，通常直到2020-01-01结束，即2020-01-02 00:00:00之后，才会开始运行涵盖2020-01-01数据周期的DAG RUN

Airflow中的所有日期在某种程度上都与数据间隔的概念相关\
例如，DAG RUN的logical date（在 Airflow 2.2之前的版本中也称为execution_date）表示数据间隔的开始，而不是DAG实际执行的时间

类似地，由于DAG及其task的start_date参数指向同一logical date，因此它标记了DAG的第一个数据间隔的开始，而不是DAG中的任务开始运行的时间\
换句话说，DAG RUN只会在start_date之后的一个间隔内启动

# 重新运行 DAG
在某些情况下，可能需要再次执行DAG\
其中一种情况是schedule的DAG运行失败时

## Catchup
使用start_date（可能还有 end_date）和非数据集计划定义的Airflow DAG定义了一系列间隔，scheduler将这些间隔转换为各个DAG RUN并执行\
默认情况下，scheduler将为自上次数据间隔以来尚未运行（或已清除）的任何数据间隔启动DAG运行，此概念称为Catchup


如果DAG不想设置Catchup（即只想当前时间点执行），那么可以将Catchup关闭，关闭后，scheduler仅为最新间隔创建DAG RUN
这可以通过以下方式关闭：
- 在DAG中设置catchup=False
- 在配置文件中设置catchup_by_default=False

```python
"""
Code that goes along with the Airflow tutorial located at:
https://github.com/apache/airflow/blob/main/airflow/example_dags/tutorial.py
"""
from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator

import datetime
import pendulum

dag = DAG(
    "tutorial",
    default_args={
        "depends_on_past": True,
        "retries": 1,
        "retry_delay": datetime.timedelta(minutes=3),
    },
    start_date=pendulum.datetime(2015, 12, 1, tz="UTC"),
    description="A simple tutorial DAG",
    schedule="@daily",
    catchup=False,
)
```

在上面的示例中，如果scheduler守护程序在2016-01-02上午6点（或从命令行）获取DAG，将创建一个数据在2016-01-01和2016-01-02之间的数据运行，下一个运行将在 2016-01-03午夜后创建，数据间隔在2016-01-02和2016-01-03之间

使用datetime.timedelta对象作为调度可能会导致不同的行为
在这种情况下，创建的单个DAG RUN将涵盖2016-01-01 06:00 和 2016-01-02 06:00之间的数据（一个调度间隔现在结束）

如果 dag.catchup 值改为 True，调度程序将为 2015-12-01 和 2016-01-02 之间的每个已完成间隔创建一个 DAG 运行（但尚未为 2016-01-02 创建一个，因为该间隔尚未完成），并且调度程序将顺序执行它们。

当在指定时间段内关闭DAG然后重新启用它时，也会触发Catchup

对于可以轻松地分成几个时期的原子数据集，这种行为非常棒
如果DAG在内部执行追赶，关闭追赶非常棒

## 回填(Backfill)
在某些情况下，可能希望为指定的历史时期运行DAG，例如，使用 start_date 2019-11-21 创建数据填充 DAG，但另一位用户需要一个月前即 2019-10-21 的输出数据。此过程称为回填。

即使在禁用追赶的情况下，您可能也希望回填数据。这可以通过 CLI 完成。运行以下命令
```cmd
airflow dags backfill \
    --start-date START_DATE \
    --end-date END_DATE \
    dag_id
```

回填命令将重新运行start date和end date内所有间隔的dag_id的所有实例

## 重新运行task
有些任务可能在schedule期间失败
在查看日志后修复错误后，可以通过clear操作来重新运行schedule date的task
clear task instance不会删除task instance的记录
相反，它将max_tries更新为0，并将当前task instance状态设置为None，这会导致任务重新运行

在树形或图形视图中单击失败的任务，然后单击清除，执行器将重新运行它

可以选择多个选项来重新运行:
- **Past：** DAG最近数据间隔之前运行中的task的所有实例
- **Future：** DAG最近数据间隔之后运行中的task的所有实例
- **Upstream：** 当前DAG中的上游任务
- **Downstream：** 当前DAG中的下游任务
- **Recursive：** 子DAG和父DAG中的所有task
- **Failed：** DAG最近运行中仅失败的task

可以使用以下命令通过 CLI 清除任务
对于指定的dag_id和time interval，该命令将清除与正则表达式匹配的所有任务实例
```cmd
airflow tasks clear {dag_id} \
    --task-regex {task_regex} \
    --start-date {START_DATE} \
    --end-date {END_DATE}
```



# 外部触发器(External Triggers)
可以通过CLI命令手动创建DAG RUN
命令：
```cmd
airflow dags trigger --exec-date {logical_date} {run_id}
```

在scheduler外部创建的DAG RUN与触发器的时间戳相关联，并与schedule的DAG RUN一起显示在UI中
DAG中传递的logical date可以使用-e参数指定
默认值是UTC时区中的当前日期。

也可以通过UI界面手工启动DAG RUN(DAGs选项卡-> column Links -> Trigger Dag按钮)



## 触发DAG时传递参数
当通过UI，rest API，或者CLI触发DAG时，可以向DAG RUn传递Json格式的配置
```python
import pendulum

from airflow import DAG
from airflow.operators.bash import BashOperator

dag = DAG(
    "example_parameterized_dag",
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
)

parameterized_task = BashOperator(
    task_id="parameterized_task",
    bash_command="echo value: {{ dag_run.conf['conf1'] }}",
    dag=dag,
)
```
dag_run.conf里的参数值只能用在operator里的template字段


### 使用CLI
```cmd
airflow dags trigger --conf '{"conf1": "value1"}' example_parameterized_dag
```

### 使用UI
在UI中，触发DAG的参数可以通过params定义更好地表示，如Params文档中所述
通过定义的参数，将呈现用于值输入的适当形式

如果DAG未定义params，通常会跳过该表单，通过配置选项show_trigger_form_if_no_params，可以强制显示仅字典输入的经典表单以传递配置选项
请考虑将此类用法转换为params，因为这是更便捷的方式，并且还允许验证用户输入
**此部分不是很理解**

# 谨记
- 在UI界面将task标记为failed时，它将会停止执行task instance
- 在UI界面将task标记为success时，此种case通常用于错误不在于该task之中，或者修复操作是在airflow之外进行的
  标记task为success有个前提，就是确保错误不能是在task之中，否则标记success会使真正的错误被忽略掉