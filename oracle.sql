----------- Window Command Settings-------------
SET WRAP OFF
COL (COLUMN_NAME) FOR A20 
set linesize 300

-- 1. make select beautiful :-)
-- 2. if set wrap off then maybe the truncating (as requested) 
--    before column xxx
-- 3.rows are maybe be truncated and can't display.

SET NLS_LANG = "SIMPLIFIED CHINESE_CHINA.ZHS16GBK"
-- `锟斤拷`
-- UTF-8 编码用 `GBK/GBK2312/GB18030` 的编码标准去解析下的错
-- 误形式(文字映射成二进制代码的格式)**.在Unicode和原有编码体系的转
-- 化过程中, 有一些字符用Unicode是无法表示的, Unicode官方用了一个占
-- 位符来表示这些无法表示的字符, 这个字符用unicode转义字符表示为
-- ufffd对应的utf-8编码为“EFBFBD”。如果这个编码重复两次, 然后放到
-- GBK/GB2312/GB1803 0的环境中显示时, 一个汉字占据2个字节, 最终的结
-- 果就是：锟斤拷——锟(EFBF), 斤(BDEF), 拷(BFBD).

-- Windows ANSI: 不是一种中文编码, 在不同的系统中, ANSI表示不同的编码
-- Refer to: 
  -- https://blog.csdn.net/amsong/article/details/39496805
  -- https://www.cnblogs.com/malecrab/p/5300486.html
  -- https://bbs.csdn.net/topics/300210062
-- More: 
  -- https://blog.csdn.net/weixin_43167418/article/details/100075486 

-- code command comment is complex in oracle (zh-environment), and I 
-- think its must write the comment in right postion such as 
-- https://docs.oracle.com/cd/B12037_01/server.101/b10759/sql_elements006.htm
-- and the comment can't appear after the character `;` (damn it....)
-- LIKE FOLLOWING THIS:
SELECT last_name,                    -- select the name
    salary + NVL(commission_pct, 0),-- total compensation
    job_id,                         -- job
    e.department_id                 -- and department
  FROM employees e,                 -- of all employees
       departments d
  WHERE e.department_id = d.department_id
    AND salary + NVL(commission_pct, 0) >  -- whose compensation 
                                           -- is greater than
      (SELECT salary + NVL(commission_pct,0)  -- the compensation
    FROM employees 
    WHERE last_name = 'Pataballa')        -- of Pataballa.
;

------------------------------------------------

startup;
dbstart
-- 启动数据库
shutdown immediate
dbshut
--停止数据库

lsnrctl start
lsnrctl stop
lsnrctl status
-- 数据库监听

sqlplus /nolog --nolog参数表示不登录, 进入sqlplus环境
-- 登陆oracle的三种方法
  -- From: https://blog.csdn.net/motianlundejiyi/article/details/8869520
-- 1. sqlplus
-- 2. url:http://127.0.0.1:xxx/isqlplus
-- 3. SQL Plus

sqlplus /nolog
conn user/passwd@ip:1521/instance_name as sysdba 
-- 远程连接数据库

SQLPLUS SYS/(password) AS SYSDBA; --SYS 表示一个权利集合的角色


CREATE USER (username) IDENTIFIED BY (password);
alter user username default tablespace username; -- 赋予用户的表空间权限
create user (username) identified by (password) default tablespace username;


GRANT DBA TO (username);
grant connect,resource,dba to username;
-- 刚刚创建完的新用户是没有任何权限的(包括登录)
-- 常用的角色 connect（7种权限）、dba、resource（在任何表空间建表）


CONN (username)/(passwd);


drop user username cascade;
-- 经常遇到如用户有对象而未加此参数则用户删不了的问题, 最好带上cascade

alter user username identified by newpassword
-- 给他人改密码


------------------------------------------------
-- from: https://pclevinblog.pixnet.net/blog/post/314561194-oracle-sql-%E7%9A%84%E5%88%86%E9%A1%9Edml%E3%80%81dcl%E3%80%81ddl
-- | TYPE          | MEANINGS     |  Notes  |
-- | ------------- | -------------|---------|
-- |DDL(Definition)| CREATE       ||
-- |               | ALTER        ||
-- |               | DROP         ||
-- |               | TRUNCATE     ||
-- |               | COMMENT      ||
-- |               | RENAME       ||
-- |DML(Manipulation)| SELECT     ||
-- |               | INSERT       ||
-- |               | UPDATE       ||
-- |               | DELETE       ||
-- |               | MERGE        |UPSERT operation (insert or update)|
-- |               | CALL         |call a PL/SQL or Java subprogram|
-- |               | EXPLAIN PLAN |explain access path to data|
-- |               | LOCK TABLE   |control concurrency|
-- |DCL(Control)   | GRANT        ||
-- |               | REVOKE       ||
-- |TCL(Transaction)| COMMIT      ||
-- |               | SAVEPOINT    ||
-- |               | ROLLBACK     ||
-- |               | SET TRANSACTION |Change transaction options like isolation level and what rollback segment to use|


------------------------------------------------
-- Create Table/Schema
CREATE SCHEMA AUTHORIZATION BGZOCG;
-- schema: 
  -- ORACLE SCHEMA is not supported?!
  -- refer to: https://stackoverflow.com/questions/10994414/missing-authorization-clause-while-creating-schema
  -- 在MySQL中,schema和database是同义词. CREATE SCHEMA和CREATE 
  -- DATABASE是等效的.但是其他的数据库产品(几乎所有数据库)有所不同.
  -- 在oracle数据库产品中,schema是database的一部分. 表示
  -- the tables and other objects owned by a single user.
-- [REFER1](https://www.cnblogs.com/zienzir/p/9093516.html)
-- [REFER2](https://blog.csdn.net/afsdfq/article/details/90417355)


-- `dual` 用法: 一个虚拟表, 构成select的语法规则, oracle保证dual里面
-- 永远只有一条记录。
-- [REFERENCE](https://www.cnblogs.com/qiangqiang/archive/2010/10/15/1852229.html)


CREATE TABLE STUDENT (
    SNO CHAR(9) PRIMARY KEY,
    SNAME CHAR(20) UNIQUE UNIQUE,
    SSEX CHAR(2),
    SAGE SMALLINT,
    SDEPT CHAR(20)
);
-- |数据类型                                |说明|
-- |----------------------------------------|----|
-- |VARCHAR2(size)                          |变长变量|
-- |CHAR(size)                              |定长变量|
-- |NUMBER(有效数字数,小数点左或右保留位数) |浮点数|
-- |DATE                                    |日期变量,也存时间|
-- |BLOB                                    |音频、视频、图形、图像|
-- |CLOB                                    |超过4000个字节的大块文本|


-- 子查询创表
CREATE TABLE new_emp_10 AS
SELECT *
FROM emp
WHERE deptno=10;


-- DELETE TABLE
DROP TABLE (TABLE_NAME) [CASCADE CONSTRAINTS]; -- !!! 命令不能回退
TRUNCATE TABLE table;-- 不能回滚记录;释放基表占用空间
--DELETE COLUMN
ALTER TABLE (tablename)
DROP COLUMN (columnname);
-- ADD COLUMN
ALTER TABLE (TABLE_NAME)
  ADD (column datatype [DEFAULT expr] [NOT NULL]
      [,column datatype]...);
ALTER TABLE (TABLE_NAME)
  DROP COLUMN column;
-- ALTER TABLE
ALTER TABLE (TABLE_NAME)
MODIFY (column datatype [DEFAULT expr] [NOT NULL]
      [,column datatype]...);


-- RENAME
-- Tables
RENAME OLD_TABLE TO NEW_NAME;
-- Constraints
ALTER TABLE (TABLE_NAME) 
RENAME CONSTRAINTS (SYS_NXXX) TO (NEW_NAME)
-- Columns
ALTER TABLE (TABLE_NAME) 
RENAME COLUMN (COLUMN_NAME) TO (NEW_NAMW)


------------------------------------------------
-- Integrity constraints 完整性约束
-- [实体完整] primary key: 表级/列级
  -- one: table or columns 表级和列级都可
  -- two: columns
-- [参照完整] foreign key: 表级/列级
create table demo(
  CONSTRAINT f_uk FOREIGN KEY(uid) REFERENCES t_user(uid)
);
-- or after creating table 
alter table demo add 
constraint f_uk
foreign key(uid) references t_user(uid);
--[用户定义] User defined:
  -- NOT NULL: 列级
  -- CHECK : 表级/列级, More to see: 
  -- https://blog.csdn.net/weixin_42187487/article/details/113051594
  -- UNIQUE: 表级/列级

-- DELETE CONSTRAINTS
ALTER TABLE (TABLE_NAME)
  DROP CONSTRAINT constraint ;
-- DISABLE/ENABLE
ALTER TABLE (TABLE_NAME)
  DISABLE/ENABLE CONSTRAINT constraint [CASCADE];


-- search constraints name
-- name: SYS_CnXXX
select user_constraints.table_name, user_constraints.constraint_name, 
constraint_type, column_name, search_condition
-- TABLE_NAME  CONSTRAINT_NAME  C  COLUMN_NAME  SEARCH_CONDITION
-- 表名         约束名       约束类型  列名       查询状态
from user_constraints, user_cons_columns
-- 查询数据字典
where user_constraints.table_name=user_cons_columns.table_name and 
user_constraints.constraint_name=user_cons_columns.constraint_name and 
user_constraints.table_name='JOB_HISTORY';

SELECT constraint_name, table_name, search_condition FROM user_constraints;


------------------------------------------------
-- insert/add data
INSERT INTO DEPT VALUES(10,'ACCOUNTING','NEW YORK'); --隐式
INSERT INTO DEPT(DEPTNO, DANAME) VALUES(60, 'MIS');-- 显式
--特定值
-- USER     变量中记录的是当前的用户信息
-- SYSDATE  变量记录当前日期和时间
-- DATE: TO_DATE
-- | FORMAT | MEANINGS|
-- |--------|---------|
-- | yy     | two  digits 两位年显示值|
-- ​| yyy    | three  digits 三位年显示值|
-- ​| yyyy   | four  digits 四位年显示值|
-- ​| Month  | |
-- ​| mm     | number两位月显示值|
-- ​| mon    | abbreviated 字符集表示 显示值|
-- ​| month  | spelled out 字符集表示 显示值|
-- ​| Day    |
-- ​| dd     | number 当月第几天显示值|
-- ​| ddd    | number 当年第几天显示值|
-- ​| dy     | abbreviated 当周第几天简写|
-- ​| day    | spelled out 当周第几天全写|
-- ​| ddspth | spelled out ordinal|
-- ​| Hour   | |
-- ​| hh     | two digits 12小时进制|
-- ​| hh24   | two digits 24小时进制|​
-- ​| Minute | |
-- ​| mi     | two  digits 60进制显示值|
-- ​| Second | |
-- ​| ss     | twodigits 60进制显示值|
-- | Other  | |
-- ​| Q      | digit 季度|
-- ​| WW     | digit 当年第几周|
-- ​| W      | digit 当月第几周|
-- 
-- TRUNC（number,num_digits)
-- by the way, the `trunc()` and `round()` handling the date type in 
-- oracle is limited by `to_char()`, in my environment the result of 
-- `select sysdate,trunc(sysdate,'dd') from dual;` is 
-- `04-JUN-21 04-JUN-21`, seems to nothing was happened.
-- So, it means that use `to_char()` when you wanna trunc the date type
-- while using `trunc()` handling the number type. 
-- meanwhile, use `round()` handling rounding number, such as
select TRUNC(123.458), --123
       TRUNC(123.458, 0), --123
       TRUNC(123.458, 1), --123.4
       TRUNC(123.458, 2), --123.45
       TRUNC(123.458, 3), --123.458
       TRUNC(123.458, 4), --123.458
       TRUNC(123.458, -1), --120
       TRUNC(123.458, -2), --100
       TRUNC(123.458, -3), --0
       TRUNC(123.458, -4), --0
       TRUNC(123), --123
       TRUNC(123, 1), --123
       TRUNC(123, 2), --123
       TRUNC(123, 3), --123
       TRUNC(123, 4) --123
  from dual;
--Round函数
select Round(123.458), --123
       Round(123.458, 0), --123
       Round(123.458, 1), --123.5
       Round(123.458, 2), --123.46
       Round(123.458, 3), --123.458
       Round(123.458, 4), --123.458
       Round(123.458, -1), --120
       Round(123.458, -2), --100
       Round(123.458, -3), --0
       Round(123.458, -4), --0
       Round(123), --123
       Round(123, 1), --123
       Round(123, 2), --123
       Round(123, 3), --123
       Round(123, 4) --123
  from dual;
-- from :https://blog.csdn.net/damaolly/article/details/25285473

-- also by the way , I found this question in following url:
-- http://www.sqlines.com/oracle-to-mysql/trunc_datetime


-- variables
INSERT INTO emp
  (empno, ename, deptno)
VALUES(&no, '&name',  &d_no);
-- 定制提示
ACCEPT dept_id PROMPT 'Please enter the department number:';
ACCEPT dept_name PROMPT 'Please enter the department name:'; 
ACCEPT region_name PROMPT 'Please enter the region number:'; 
INSERT INTO dept (deptno, dname, loc) VALUES (&dept_id, ‘&dept_name’, ‘&region_name’);
-- 子查询
CREATE TABLE new_emp AS
SELECT *
FROM emp
WHERE deptno=10;


-- comment 注释
COMMENT ON COLUMN EMP.JOB IS '工作';


--UPDATE
UPDATE (table-name)
  SET (column)=(value) [,column=value] 
  [ WHERE condition];
--where 缺省时表内元素全部修改


-- delete data
DELETE [FROM] table [WHERE condition];
DELETE FROM (table_name);


------------------------------------------------
COMMIT;
SAVEPOINT A;
-- ....
ROLLBACK TO A;


------------------------------------------------
-- Select语句的一般形式
SELECT [ALL|DISTINCT]
<目标列表达式> [别名] [ ，<目标列表达式> [别名]] …
FROM <表名或视图名>[别名] [ ，<表名或视图名> [别名]] …
[WHERE <条件表达式>]
[GROUP BY <列名1>
[HAVING <条件表达式>]]
[ORDER BY <列名2> [ASC|DESC]
-- 单表查询
  -- 多重条件查询AND的优先级高于OR
-- 目标列表达式
  --算术表达式/字符串常量/函数/列别名
-- ORDER BY子句; ASC(ascending)/DESC(descending)
SELECT Sno, Grade
FROM SC
WHERE Cno= '3'
ORDER BY Grade DESC
-- 聚集函数: count(*)：获取数量; sum()：求和（这里要注意求和是
-- 忽略null值的，null与其他数值相加结果为null，所以可以通过
-- ifnull(xxx,0)将null的值赋为0）; avg()：求平均数; max()：求最大值; 
-- min()：求最小值
-- GROUP BY: 细化聚集函数的作用对象
SELECT city, count(*), age
FROM dbo.user
WHERE departmentID=2
GROUP BY city,age
HAVING age >40  --where 不可以使用聚集函数
-- 执行顺序[WGAH]: where,group by,having及聚集函数(aggr)时,顺序：
  -- 执行where子句查找符合条件的数据；
  -- 使用group by 子句对数据进行分组；
  -- 对group by 子句形成的组运行聚集函数计算每一组的值；
  -- 最后用having 子句去掉不符合条件的组


------------------------------------------------
-- 嵌套查询


------------------------------------------------
-- 连接查询
-- (非)等值(=) from https://blog.csdn.net/jiakw_1981/article/details/3050917
--  等值连接中不要求相等属性值的属性名相同，而自然连接要求相等属性值的属性名必须相同，即两关系只有在同名属性才能进行自然连接。
-- 自然连接是去掉重复列的等值连接, 等值连接不将重复属性去掉，而自然连接去掉重复属性，也可以说。
SELECT STUDENT.*, SC.*
FROM STUDENT, SC (
WHERE STUDENT.SNO=SC.SNO
);

--自身连接
SELECT FIRST.*, SECOND.*
FROM COURSE FIRST, COURSE SECOND
WHERE FIRST.CPNO=SECOND.CNO;

--外连接: 将主体表中不满足连接条件的元组一并输出
SELECT Student.Sno, Sname, Ssex, Sage, Sdept, Cno, Grade
FROM Student
LEFT/RIGHT/ALL (OUTER/INNER) JOIN SC ON
(Student.Sno=SC.Sno);
-- FROM Student LEFT OUTER JOIN SC USING(Sno)
-- See img diff with each other: 
-- ![](https://.oss-cn-beijing.aliyuncs.com/Visual_SQL_JOINS_orig.webp) 
-- and from its from: 
-- https://www.codeproject.com/Articles/33052/Visual-Representation-of-SQL-Joins

-- 复合条件连接: 多个连接条件
SELECT Student.Sno, Sname
FROM Student, SC
WHERE Student.Sno = SC.Sno AND /* 连接谓词*/
  SC.Cno= '2' AND SC.Grade > 90; /* 其他限定条件 */


------------------------------------------------
-- 嵌套查询 不能使用ORDER BY子句
-- IN 谓词, 只存在一个子结果的时候 = 可以代替 In
-- 比较运算符(>，<，=，>=，<=，!=或<>), 与ANY或ALL谓词配合
-- 带有ANY（SOME）(任意一个值)或ALL(所有值)谓词的子查询
-- 带有EXISTS谓词的子查询
-- 不相关子查询
SELECT Sno, Sname, Sdept
FROM Student
WHERE Sdept IN
(SELECT SDEPT
FROM STUDENT
WHERE SNAME='刘晨');


-- 相关子查询: 子查询联系父查询(子句 where 条件里用到父句的表)
SELECT Sno, Cno
FROM SC x
WHERE Grade >=(SELECT AVG(Grade)
FROM SC y
WHERE y.Sno=x.Sno);


-- 带有ANY（SOME）或ALL谓词
SELECT Sname, Sage
FROM Student
WHERE Sage < ANY (SELECT Sage
  FROM Student
  WHERE Sdept= 'CS')
  AND Sdept <> 'CS' ;
/* WHERE Sage < (SELECT MAX(Sage) FROM Student WHERE Sdept= ' CS ') */

-- 带有EXISTS谓词: EXISTS的子查询只返回真值或假值，给出列名无实际意义
-- 所有带IN谓词、比较运算符、ANY和ALL谓词的子查询都能用带 EXISTS谓词的子查询等价替换
SELECT Sname
FROM Student
WHERE NOT EXISTS(SELECT *
FROM Course
WHERE NOT EXISTS(SELECT *
FROM SC
WHERE Sno= Student.Sno
  AND Cno= Course.Cno)
); --查询选修了全部课程的学生姓名

-- 用EXISTS/NOT EXISTS实现逻辑蕴函(难)
-- 查询至少选修了学生200215122选修的全部课程的学生号码
SELECT DISTINCT Sno
FROM SC SCX
WHERE NOT EXISTS
(SELECT *
FROM SC SCY
WHERE SCY.Sno = ' 200215122 ' AND NOT EXISTS (SELECT *
  FROM SC SCZ
  WHERE SCZ.Sno=SCX.Sno AND SCZ.Cno=SCY.Cno));

-- 集合查询
-- 并操作 UNION `UNION`: 自动去重; `UNION ALL` 不去重(DISTINCT)
-- 交操作 INTERSECT
-- 差操作 EXCEPT(MINUS)
  SELECT *
  FROM Student
  WHERE Sdept= 'CS'
UNION
  SELECT *
  FROM Student
  WHERE Sage<=19
-- OR

-- 既选修了课程1又选修了课程2 的学生
SELECT Sno
FROM SC
WHERE Cno='1' AND Sno IN (SELECT Sno
  FROM SC
  WHERE Cno='2')

-- 基于派生表(Derived Table)的查询: 出现在FROM的子查询
-- 找出每个学生超过他自己选修课程平均成绩的课程号
SELECT Sno, Cno
FROM SC, (SELECT Sno, Avg(Grade)
  FROM SC
  GROUP BY Sno) AS Avg_sc (avg_sno, avg_grade)
WHERE SC.Sno = Avg_sc.avg_sno and SC.Grade >=Avg_sc.avg_grade ;
/* 此处 (SELECT Sno, Avg(Grade) FROM SC GROUP BY Sno) AS 
 * Avg_sc (avg_sno, avg_grade) 为临时表
*/

/**********************************************
AVG (DISTINCT|ALL|n)            平均值
COUNT (DISTINCT|ALL|expr|*)     计算个数
MAX (DISTINCT|ALL|expr)         最大值
MIN (DISTINCT|ALL|expr)         最小值
STDDEV (DISTINCT|ALL|n)         标准差
SUM (DISTINCT|ALL|n)            求和
VARIANCE (DISTINCT|ALL|n)       方差
COUNT(*)                        返回表中的记录数
COUNT(expr)                     返回非空记录数
***********************************************/


-- View
CREATE [OR REPLACE] [FORCE|NOFORCE] VIEW view 
  [(alias[, alias]...)] 
  AS sub-query 
  [WITH CHECK OPTION [CONSTRAINT constraint ]] -- impact update data
  [WITH READ ONLY]
DROP VIEW (VIEW_NAME);

-- DML operation only impact the single view table.


/******************REFERENCE*******************
- https://www.nginx.cn/6235.html
- https://kangdonggen.gitbooks.io/oracle/content/chapter1.html
***********************************************/