lock
用于锁表，当使用lock锁住某一张表时，该表不能被其他会话对其进行增删改查操作
lock的生命周期为，从lock开始到下一个commit结束
URL： https://docs.amazonaws.cn/redshift/latest/dg/r_LOCK.html

```sql
lock tableA;

/*
statement...
该区间代码执行期间，其他会话不可以对tableA表进行增删改查操作
*/

commit;
/*
statement...
该区间代码执行期间，其他会话可以对tableA表进行增删改查操作
*/

```