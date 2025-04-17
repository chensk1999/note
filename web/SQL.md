SQL（结构化查询语言，Structured Query Language）是一种用来访问和操作数据库的语言，它是高级的非过程语言。SQL语言已经被ISO标准化，各种数据库程序对标准SQL有不同的扩展。SQL关键字不区分大小写，表名和列名有的数据库区分，有的不区分

# 数据库理论

## 数据库管理系统（DBMS）

数据库管理系统（database management system, DBMS）是一种用来组织、储存、管理数据的系统。相比于直接把数据存在文件里，把数据交给数据库管理系统来管理有许多优势，比如

1. 不需要每个程序都进行文件读写和数据解析
2. 提供了通用的数据接口，方便数据复用
3. 设计合理的数据库能够简化数据结构，避免冗余和数据一致性问题
4. 数据访问/修改权限限制

## 数据模型（data model）

数据模型是描述数据之间逻辑关系的方法。当前绝大多数数据库都属于关系模型，称作关系数据库（Relational Database，RDB）。其他模型主要在一些特殊场景使用。许多人热衷于研究新的模型，想取代RDB的地位

## 关系模型

关系数据库由若干二维表构成，每个表有唯一的名字，表的每一行称作记录（record），每一列称作字段（column），标识某项记录的字段称作键（key）。表中每一项都是不可分的，即不能在表中包含表

另一种叫法（可能是比较教科书的叫法？），把一张表称作关系（relation），每行称作元组（tuple），元组的某个属性值叫做分量，每列称作属性（attribute），标识项称作码（key），属性取值范围叫做域（domain）

### 键（key）

关系表要求不能有重复记录，应用中通常选择一个字段作为区分的标识符，称作**主键（primary key）**。变更主键会带来大量的问题，因此常创建一个与业务无关的键（id）作为主键，常用的创建方法有自增整数、全局唯一GUID。注意int类型大小限制了整数id的个数

### 关系之间的引用

上一个例子是多对一的外键（多个学生对应一个班级），经常还会有一对多、多对多、一对一（如每个学生对应一个手机号。不把手机号放进学生表里可能是为了不改动学生表，或有的学生没有手机号，或者把不常用的字段分开存储提高效率）

多对一、一对多
多个学生对一个专业，如果从专业角度来看就是一个专业对多个学生
学生（学号，姓名，专业号）
专业（专业号，专业名）

多对多
多个学生对多个课程
学生（学号，姓名，课程号）
课程（课程号，课程名，学分）
修读情况（学号，课程号，成绩）

一对一
一个学生对一个电话号码。使用一对一的原因可能有：给原本数据库添加联系方式而不改变原本的学生表、把大表中不常用的字段拆出来，提高查询效率
学生（学号，姓名）
联系方式（学号，电话号码）

### 索引

索引是对某一列的值进行预排序的数据结构，使用索引后查找时不会搜索整张表而是直接定位，加快查询速度，但代价时插入、更新、删除时索引要变化，因此这些操作的速度下降。

## 数据库设计

- **需求分析**：需求主要包括信息要求（存储哪些信息）、处理要求、安全性与完整性要求，分析流程是熟悉业务、明确需求、确定系统边界。此阶段主要成果是数据字典
- **概念结构设计**：将应用需求抽象为直接反应现实世界、便与理解、便于修改的概念模型。常用E-R模型表示，用矩形表示实体，椭圆形表示属性，菱形表示联系，把每个实体与其属性连起来，每个联系与有关实体、属性连起来，连线旁标注类型(1:1, 1:n, m:n)。凡是不需要另外描述、只与一个实体联系的事物，都可以当作属性看待。为了简便，能当作属性的都应该当作属性
- **逻辑结构设计**：从E-R图到关系模型
- 物理结构设计、实施与维护……

# 数据类型

| 名称         | 类型           | 说明                                                         |
| ------------ | -------------- | ------------------------------------------------------------ |
| INT          | 整型           | 4字节整数类型，范围约+/-21亿                                 |
| BIGINT       | 长整型         | 8字节整数类型，范围约+/-922亿亿                              |
| REAL         | 浮点型         | 4字节浮点数，范围约+/-1038                                   |
| DOUBLE       | 浮点型         | 8字节浮点数，范围约+/-10308                                  |
| DECIMAL(M,N) | 高精度小数     | 由用户指定精度的小数，例如，DECIMAL(20,10)表示一共20位，其中小数10位，通常用于财务计算 |
| CHAR(N)      | 定长字符串     | 存储指定长度的字符串，例如，CHAR(100)总是存储100个字符的字符串 |
| VARCHAR(N)   | 变长字符串     | 存储可变长度的字符串，例如，VARCHAR(100)可以存储0~100个字符的字符串 |
| BOOLEAN      | 布尔类型       | 存储True或者False                                            |
| DATE         | 日期类型       | 存储日期，例如，2018-06-22                                   |
| TIME         | 时间类型       | 存储时间，例如，12:20:59                                     |
| DATETIME     | 日期和时间类型 | 存储日期+时间，例如，2018-06-22 12:20:59                     |

# 访问数据库、表

数据定义语言（data define language, DDL）

## 定义数据库

```sql
SHOW DATABASES;  -- 查询数据库列表
CREATE DATABASE school;  -- 创建
USE school;      -- 选择数据库
SHOW TABLES;     -- 查询当前数据库所有表
DESC students;   -- 查询表的结构，字段类型，主键，是否为空等属性
DROP school;     -- 删除表
```

## 定义表

```sql
CREATE TABLE students(
    id INT UNSIGNED AUTO_INCREMENT,
    class_id INT UNSIGNED DEFAULT 1,
    name VARCHAR(100) NOT NULL comment "姓名",
    score INT UNSIGNED comment "分数",
    PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;  -- 设置存储引擎和编码
```

## 修改表

```sql
ALTER TABLE students ADD gender CHAR(1) NOT NULL AFTER name;  -- 添加字段
ALTER TABLE students DROP gender;             -- 删除字段
ALTER TABLE students CHANGE score points int; -- 修改字段名
ALTER TABLE students RENAME pupil;            -- 修改表名
DROP TABLE students;                          -- 删除表

-- 修改约束
ALTER TABLE students ADD CONSTRAINT unique_name UNIQUE(name);
ALTER TABLE students DROP INDEX unique_name;
```

# 修改数据

数据操作语言（data manipulation language, DML）

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

# 查询数据

SQL主要用`SELECT`指令查询。查询结果是一张表


```sql
-- 基础查询
SELECT *                               -- 要查询的列
FROM students                          -- 表名
WHERE score > 90 AND NOT class_id = 1  -- 查询条件
ORDER BY score DESC, id;               -- 排序。例子中按分数降序，同分的按id排序

-- 后面三项都可以省略。全省略时可用来检查数据库连接
SELECT 1;
```

常用条件表达式有：

| 表达式            | 含义                                                   |
| ----------------- | ------------------------------------------------------ |
| `>, <, =, >=, <=` | 比较。注意相等只有一个等号                             |
| `<>`              | 不等于                                                 |
| `REGEXP 'reg'`    | 正则表达式                                             |
| `BETWEEN`         | 区间                                                   |
| `IS NULL`         | 是否`NULL`（注意：`NULL`和其他值比较结果始终为`NULL`） |
| `<=>`             | 两个值相等或者都为`NULL`                               |

**复杂查询**

```sql
-- 分页查询
SELECT * FROM students LIMIT 50 OFFSET 20;  -- 显示50条，从第20条开始显示
SELECT * FROM students LIMIT 20, 50;        -- 相同作用

-- 聚合查询。SQL提供了COUNT, SUM, AVG, MAX, MIN等聚合函数
-- 如果没有匹配到任何内容（比如配合WHERE使用时），COUNT为0，其他几个为NULL
SELECT AVG(score) average FROM students;  -- 查询平均分，结果是一行一列的表，列名设为average

-- 分组
SELECT COUNT(*) num FROM students GROUP BY class_id;
    -- 按照class_id分组，分别统计个数。返回class_id个数列、1行的表
SELECT class_id, COUNT(*) num FROM students GROUP BY class_id;
    -- 两列，第一列为class_id，第二列为count
    -- 如果投影到非聚合函数的列，并且这一列在每一组中不全一样，会报错
SELECT class_id, gender, COUNT(*) num FROM students GROUP BY class_id, gender;
    -- 使用多个列进行分组，此例的结果将是班级数量*2（男女两个性别）列、3行的表

-- 笛卡尔查询
SELECT * FROM students, classes;
    -- 查询结果是两个表的直积，即表1与表2每行两两拼起来，有c1+c2列，r1*r2行
    -- 如果两张表有重复的表头，查询结果就会有重复表头，可以设置别名来解决
SELECT
    s.id sid,
    s.name,
    c.id cid,
    c.name cname
FROM students s, classes c;

-- 连接查询
SELECT students.id, students.name, class.name class_name
FROM students
INNER JOIN classes
ON students.class_id = classes.id;
/*
以students作为主表，连接classes表，连接条件是classes.id = students.class_id的条目
INNER JOIn表示只返回同时存在于两张表的数据；LEFT OUTER JOIN则返回全部右表存在的行，如
只在右表存在，空余列填NULL；RIGHT OUTER JOIN反之，FULL OUTER JOIN返回全部的行
*/

-- 并集
SELECT * from students WHERE class_id=1
UNION
SELECT * from students WHERE class_id=2;
```

# 事务

事务是SQL操作的单元，事务具有ACID这4个特性：

- A：Atomic，原子性，事务要么全部执行，要么全部不执行
- C：Consistent，一致性，事务完成后，所有数据的状态都是一致的，比如A账户只要减去了100，B账户则必定加上了100
- I：Isolation，隔离性，如果有多个事务并发执行，每个事务作出的修改必须与其他事务隔离
- D：Duration，持久性，即事务完成后，对数据库数据的修改被持久化存储

单条SQL语句是隐式事务，也可以声明显示事务

```sql
BEGIN;
-- 语句
COMMIT;
```

不同事务分隔有Read Uncommited, Read Commited, Repeatable Read, Serializable四个，前三个在并行执行时都有不同程度的问题，最后一个串行执行事务，不会遇到问题，但是性能大大下降

# 函数



# SQL数据库

## MySQL

```bash
# 登录。-u参数为用户名，-p参数表示需要密码
mysql -u root -p

# 登录成功后会显示SQL shell。在此输入SQL语句即可访问数据库
mysql>
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
