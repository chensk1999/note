# 数据库理论

## 数据库管理系统

数据库管理系统（database management system, DBMS）是一种用来组织、储存、管理数据的系统。相比于直接把数据存在文件里，把数据交给数据库管理系统来管理有许多优势，比如

1. 不需要每个程序都进行文件读写和数据解析
2. 提供了通用的数据接口，方便数据复用
3. 设计合理的数据库能够简化数据结构，避免冗余和数据一致性问题
4. 数据访问/修改权限限制

数据库可以分为两类：

- **关系数据库**（Relational Database，RDB）：将数据存储为表，每行存储一条记录，表中的列用于存储该记录的属性。RDB是目前最成熟、应用最广泛的数据库
  - MySQL，PostgreSQL，Oracle，MSSQL，SQLite等

- **非关系数据库**（Non-SQL，NoSQL）：使用关系模型以外的结构存储数据。主要用于关系数据库性能不佳的场景，例如缓存、文件索引。在综合表现上，非关系数据库各有自己的短板，目前没有任何一个非关系数据库的表现在一般场景下能接近RDB
  - 键值数据库：典型代表有Redis，Memcached。每条数据是键值对，值可以是任意对象，通过键快速定位对应的值。常用于缓存
  - 文档数据库：如MongoDB，数据同样以键值对组织，值是嵌套对象（如Json文档），可用于存储、检索没有固定结构的对象

## 关系模型

关系数据库（Realtional Database，RDB）由若干二维表构成，每个表有唯一的名字，表的每一行称作记录（record），每一列称作字段（column），标识某项记录的字段称作键（key）。表中每一项都是不可分的，即不能在表中包含表

关系代数中，将一张表称作关系（relation），每行称作元组（tuple），元组的某个属性值叫做分量，每列称作属性（attribute），标识项称作码（key），属性取值范围叫做域（domain）。关系数据库理论偶尔会采用这种称呼。本笔记采用实践中更常用的表、行、字段叫法

需要注意，关系是元组的集合，因此是无序的，并且一个表中不能有两个完全相同的行。实践中通常用一个字段区分不同记录，称作**主键（primary key）**

变更主键会带来大量的问题，因此常创建一个与业务无关的键作为主键，常用的创建方法有自增整数、全局唯一GUID。注意int类型大小限制了整数id的个数

### 关系之间的引用

- 多对一、一对多
  - 多个学生对一个专业。如果从专业角度来看就是一个专业对多个学生
  - 设计两张表：学生（学号，姓名，专业号）、专业（专业号，专业名），利用`学生`表的`专业号`字段表示学生和专业的引用
- 多对多
  - 多个学生对多个课程
  - 设计三张表：学生（学号，姓名，课程号）、课程（课程号，课程名，学分）、修读情况（学号，课程号，成绩），利用`修读情况`表记录记录之间的引用
- 一对一
  - 一个学生对一个电话号码。使用一对一的原因可能有：给原本数据库添加联系方式而不改变原本的学生表、把大表中不常用的字段拆出来，提高查询效率
  - 设计两张表：学生（学号，姓名）、联系方式（学号，电话号码）

可以对引用作出**参照完整性约束**：被参照实体先插入、后删除。以学生表引用专业号为例，必须先插入专业，再插入该专业的学生；必须先删除该专业所有学生，再删除该专业。实际工程中满足这些约束可能较麻烦，也可能引起性能问题（因为插入和删除都要锁住被参照的表）

### 索引

索引是对某一列的值进行预排序的数据结构，使用索引后查找时不会搜索整张表而是直接定位，加快查询速度，但代价是插入、更新、删除时索引要变化，因此这些操作的速度下降

# SQL

结构化查询语言（Structured Query Language，SQL）是用来管理关系数据库的语言。各个RDB软件使用的语言略有区别（有的并未完全实现ISO标准，或是对标准SQL加入了自己独有的扩展语法），但大部分功能仍可互通。不通用的语法本笔记中会特别注明

SQL分为四种语句：

- 数据定义语言（data define language, DDL）
- 数据查询语言（Data Query Language，DQL）
- 数据操作语言（data manipulation language, DML）
- 事务控制语言（Transaction Control Language，TCL）

分别对应后文定义数据库、查询数据、修改数据、事务控制四节

## 定义数据库、表

### 定义数据库

```sql
SHOW DATABASES;  -- 查询数据库列表
CREATE DATABASE school;  -- 创建
USE school;      -- 选择数据库
SHOW TABLES;     -- 查询当前数据库所有表
DESC student;   -- 查询表的结构，字段类型，主键，是否为空等属性
DROP school;     -- 删除数据库
```

### 定义表

```sql
CREATE TABLE student(
    id       INT UNSIGNED AUTO_INCREMENT,
    class_id INT UNSIGNED DEFAULT 1,
    name     VARCHAR(100) NOT NULL,
    score    INT UNSIGNED,
    PRIMARY KEY (id)
);
```

### 修改表

```sql
ALTER TABLE student ADD gender CHAR(1) NOT NULL AFTER name;  -- 添加字段
ALTER TABLE student DROP gender;             -- 删除字段
ALTER TABLE student CHANGE score points int; -- 修改字段名
ALTER TABLE student RENAME pupil;            -- 修改表名
DROP TABLE student;                          -- 删除表

-- 修改约束
ALTER TABLE student ADD CONSTRAINT unique_name UNIQUE(name);
ALTER TABLE student DROP INDEX unique_name;
```

## 查询数据


```sql
-- SELECT语句示例。从students表中筛选id=1的学生，查询其姓名和分数
SELECT name, score FROM student WHERE id=1;

-- 后面的子句都可以省略。全省略时可用来检查数据库连接
SELECT 1;
```

完整`SELECT`语句。下面例子计算人数大于20人的班级的女学生的平均分

```sql
SELECT AVG(student.score), class.id -- 查询字段
FROM                                -- 数据来源。可以是表名、笛卡尔积、JOIN等
    student INNER JOIN class
    ON student.class_id=class.id
WHERE gender='F'            -- 查询条件
GROUP BY class.id           -- 分组
HAVING count(class.id)>20   -- 筛选条件
UNION select 60, -1         -- 联合查询
ORDER BY student.score;     -- 排序
LIMIT 5, 1                  -- 分页查询
INTO OUTFILE 'out.txt';     -- 保存结果到文件
```

执行时，每一步生成一张虚拟表`vt`作为下一步的输入。各语句执行顺序如下

1. **From**：从选中的表生成虚拟表`vt1`，然后筛选出满足**On**语句的表`vt2`，并根据**Join**语句把上一步筛掉的行加回去生成`vt3`
2. **Where**：筛选生成`vt4`
3. **Group By**：计算聚合函数并整合为`vt5`。如果有**With Rollup**语句则再生成为`vt6`
4. **Having**：对分组后的数据再筛选一次得到`vt7`
5. **Select**：把需要的列筛出来得到`vt8`。如果有**Distinct**则筛选得到`vt9`
6. **Order By**：排序并返回游标（关系数据表是无序的，因此使用另一种数据结构表达其顺序）
7. **Limit**：返回需要的行数

### Select - 查询字段

可以是字段名、表达式

```sql
SELECT * FROM student;            -- 查询全部列
SELECT name, score FROM student;  -- 查询name, score两列
SELECT MAX(score) FROM stdent;    -- 查询最高分。常用聚合函数：COUNT, SUM, AVG, MAX, MIN
SELECT DISTINCT class_id FROM student;  -- DISTINCT关键字对完全相同的行去重（选择多列时，需要每列都相同）
```

还可以给查询字段起别名

```sql
SELECT
    id as sid,       -- 用as标识别名
    name `sname`,    -- 反斜杠标识别名
    gender sgender   -- 空格，同样也是表示别名
FROM student as s;   -- 表名也可以起别名
```

### From - 数据来源

```sql
-- 单个表
SELECT * FROM students;
-- 笛卡尔积。即表1与表2每行两两拼起来，有c1+c2列，r1*r2行
SELECT s.name, s.class_id, c.id FROM student as s, class as c;
```

`JOIN`语句拼接两个表。`ON`语句定义了拼接规则，下面例子中将`student.class_id`和`class.id`相同的行拼接起来。`JOIN`语句可以用关键词控制选择范围：`INNER JOIN`返回成功拼接的行；`LEFT JOIN`包括了左边表全部行，拼接失败的行右边部分是`NULLs`；`RIGHT JOIN`包括右边表全部行；`FULL JOIN`包含两边的全部行

```sql
SELECT student.name, class.name
FROM student INNER JOIN class
ON student.class_id = class.id;
```

### Where - 查询条件

常用条件表达式有：

| 表达式                    | 含义                                                   |
| ------------------------- | ------------------------------------------------------ |
| `>, <, =, >=, <=`         | 比较。注意相等只有一个等号                             |
| `<>`                      | 不等于                                                 |
| `LIKE 'a%', REGEXP 'reg'` | 字符串匹配、正则表达式                                 |
| `BETWEEN 1 AND 2`         | 区间                                                   |
| `IS NULL`                 | 是否`NULL`（注意：`NULL`和其他值比较结果始终为`NULL`） |
| `<=>`                     | 两个值相等或者都为`NULL`                               |

### Group By - 分组

Group By语句对数据分组进行统计。下面第一个例子根据统计各班级人数；第二个例子统计各班级各性别人数

```sql
SELECT class_id, COUNT(*) num FROM student GROUP BY class_id;
SELECT class_id, gender, COUNT(*) num FROM student GROUP BY class_id, gender;
```

### Having - 筛选

Having子句可以筛选聚合、分组后的数据

```sql
SELECT class_id, AVG(score) FROM student
GROUP BY class_id
HAVING AVG(score)>80;
```

### Union - 联合查询

相当于两张表上下拼起来。两个查询列数必须相同

```sql
SELECT name, score FROM student
UNION SELECT '及格线', 60;

SELECT name, score FROM student
UNION ALL SELECT '李华', 80;  -- UNION默认去除重复行；UNION ALL不会
```

### Order By - 排序

```sql
-- 按照列名排序、按照第几列排序
SELECT * FROM student ORDER BY name ASC, class_id DESC;
SELECT * FROM student ORDER BY 1;
-- 按照表达式排序
SELECT * FROM student ORDER BY CHAR_LEN(name);
```

### Limit - 分页

```sql
SELECT * FROM student LIMIT 10 OFFSET 20;  -- 显示10条，从第21条开始显示
SELECT * FROM student LIMIT 20, 10;        -- 相同作用

-- MSSQL、Oracle写法
SELECT * FROM student ORDER BY name FETCH FIRST 10 ROWS ONLY;
SELECT * FROM student ORDER BY name OFFSET 20 ROWS FETCH NEXT 10 ROWS ONLY;

SELECT TOP 10 * FROM students;            -- MSSQL旧版本写法
SELECT * FROM students WHERE ROWNUM < 10; -- Oracle旧版本写法
```

### 嵌套查询

可以在SELECT、INSERT等语句中嵌套SELECT语句，

```sql
-- 用括号括起子查询语句
-- 如果子查询返回值只有一个，可以用比较运算符当作数值处理
SELECT * FROM person WHERE age > (select age from persom where name='John Doe');

-- 如果子查询返回值是n行1列，可以用any，all，in等运算符处理
SELECT * FROM person WHERE country_id in (select id from country where population > 1e7);

-- 如果子查询有多行多列，可以当作一个表来处理
SELECT s.id
FROM (select * from student)s;  # 注意，最后的s是给这个表起的别名。必须有别名才会被当作一个表
```

## 修改数据

```sql
-- 插入
INSERT INTO students (class_id, name, gender, score)
VALUES (2, '大牛', 'M', 80)
ON DUPLICATE KEY UPDATE;  -- 可选，如果UNIQUE索引或主键冲突则更新

INSERT IGNORE INTO /*表，字段，值*/  -- 如果冲突则忽略

-- 更新
UPDATE students SET score=66 WHERE id=1;
UPDATE students SET score=score+10 WHERE score<80;

-- 删除
DELETE FROM students WHERE id=1;

-- 替换，如果该记录存在，则删除并插入新记录；否则，插入新记录
REPLACE INTO students (id, class_id, name, gender, score) VALUES (1, 1, '小明', 'F', 99);
```

## 事务控制

事务（Transaction）是SQL操作的单元，事务具有ACID特性：

- 原子性（**A**tomic）：事务要么全部执行，要么全部不执行
- 一致性（**C**onsistent）：事务不会破坏数据完整性（如主键唯一、字段类型大小符合约束）
- 隔离性（**I**solation）：如果有多个事务并发执行，每个事务作出的修改必须与其他事务隔离
- 持久性（**D**uration）：即事务完成后，对数据库数据的修改被持久化存储

单条SQL语句是隐式事务，也可以显示声明事务

```sql
BEGIN;
-- 语句
COMMIT;
```

注意：虽然SQL标准规定事务要有ACID特性，但并不是每个数据库都完全实现ACID。比如MySQL的DDL语句不满足原子性

# SQL数据库

## MySQL

```bash
# 启动mysql服务器（具体命令因版本可能不同）
service mysql start

# 登录。-u参数为用户名，-p参数表示需要密码（可能需要sudo）
mysql -u root -p

# 登录成功后会显示SQL shell。在此输入SQL语句即可访问数据库
mysql>
```

用户管理

```sql
CREATE USER 'your_name' IDENTIFIED BY 'password';
GRANT all privileges ON db_name.* TO your_name@localhost IDENTIFIED BY 'password';
SHOW GRANTS FOR your_name;
```

## Python Connector

将SQL嵌入到高级语言中混合编程，SQL语句负责操纵数据库，高级语言负责控制逻辑，称为嵌入式SQL，重点在于两种语言之间的通信

```python
import mysql.connector

#登录到MySQL服务器
config = {
  'user': 'scott',
  'password': 'password',
  'host': '127.0.0.1',
  'database': 'employees',
  'raise_on_warnings': True
}  #把配置放在config文件，不要写进代码！
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

#执行SQL指令
op = ''       #some sql operations，可以用格式化字符串（%s等）
param = ''    #值的tuple，对应格式化字符串中的值
cursor.execute(op, param)

#如果使用查询语句，结果是一个表，依据表的大小，有多种处置方法
#常用的一个是将cursor当作iterator，产生每一行的tuple

cnx.commit()
cursor.close()
cnx.close()
```
