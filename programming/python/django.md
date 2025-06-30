# 基础

```powershell
# 安装
pip install django

# 创建项目，注意用保留词（比如Django，test）做项目名会出问题
python -m django startproject mysite
cd mysite

# 创建网页应用
python manage.py startapp myapp

# 运行服务器，并允许局域网访问
manage.py runserver 0.0.0.0:8000
```

完成以上步骤之后在浏览器输入`localhost:8000`或者`本机ip:8000`，能看到示例页面。若出现访问权限等问题，需要在`sesttings.py`的`ALLOWED_HOSTS`列表中添加请求访问的设备的ip地址，例如`ALLOWED_HOSTS = ['114.210.194.92']`

## 设计模式

Django使用MVT设计模式。MVT指Model，View，Template，它们分别负责数据库操作、业务逻辑、页面渲染

1. 用户发出请求，Django接收到请求后，根据`urls.py`的配置调用`view`函数
2. `views.py`中的`view`函数执行业务逻辑。需要操作数据库时调用`models.py`中的`model`类访问数据库（换句话说，`model`把SQL操作包装好，业务逻辑使用`model`作为中介访问数据库）
3. 读取`template`文件，渲染为最终呈现给用户的样子，最后返回响应

```mermaid
graph LR
  user[/用户/] <--> View(View: 业务逻辑)
  View <---> Model(Model: 数据库操作)
  Model <--> Database[(Database)]
  View ---- Template(Template: 页面样式)
```

另一种常见的设计模式是MVC（Model View Controller），它是MVT的前身。**Controller**接收用户的请求，并选择相应的Model去处理；**Model**操作数据库；最后**View**将数据显示给客户端用户

```mermaid
graph LR
  1[/User/] --> C(Controller) 
  C --> M(Model)
  M --> V(View)
  V --> 2[/User/]
```

MVC模式中页面样式和数据仍有耦合；MVT模式模块间耦合更低。因此MVT更容易扩展

## 工作流程

1. 创建项目。`python django-admin.py startproject mysite`
2. 创建应用。`python manage.py startapp myapp`
3. URL路由规则和View。这两个写好之后就能提供基本的服务了

```python
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

# 放在urls.py
# 第一个参数是URL规则，尖括号内的作为关键字参数传给View；第二个参数是View函数
urlpatterns = [
    path('admin/', admin.site.urls),
    path('articles/<slug:title>/<int:section>/', view),
]

# 放在views.py，负责构造HTTP响应
def view(request, title:str, section:int):
    return HttpResponse(f'{title}</br>section {section}')
```

较复杂的网站应使用多级路由。这种写法将应用间耦合减到最低，只要有多个应用，就应该用这种写法

```python
from django.urls import include

urlpatterns = [
    path('myapp/', include(myapp.urls)),
]
```

# View

View执行业务逻辑，并通过Model操纵数据库、通过Template生成网页代码，最终返回完整网页

```python
from django.shortcuts import render

def response(request):
    context = {'hello': 'Hello, world!', 'list':[0], 'dict':{'a':1}}
    return render(request, 'template.html', context)
```

# Template

Template是网页前端的HTML、CSS和Javascript文件，它们通常还需要填入数据才能显示给用户看。HTML模板一般格式为：

```html
<!-- template.html -->

<h1>
    {{ hello }}
    {{ list.0 }}
    {{ dict.a }}
    <!-- 待填入的数据用双大括号括起来。注意索引用点而不是方括号 -->
    <!-- 数据由View负责填充-->
</h1>
```

然后在`settings.TEMPLATES.DIRS`里面加入模板所在文件夹，比如`TEMPLATES['DIR'] = BASE_DIR / 'templates'`

## 控制流

```html
<!-- if分支 -->
<p>
    {% if cond1 and cond2 %}
        cond1和cond2均为真
    {% elif cond1 %}
        cond1为真，cond2为假
    {% else %}
        cond1为假
    {% endif %}
</p>

<!-- for循环迭代列表 -->
{% for paragraph in paragraph_list %}
    <p>{{ paragraph }}</p>
{% empty %}
    <p>没有文章</p>
{% endfor %}

<!-- for循环迭代字典 -->
{% for name, url in images.items %}
    <img src="{{ url }}" alt="{{ name }}" />
{% endfor %}
```

除了上面写了的用法之外，还可以在循环内用循环变量`forloop.counter`循环次数、`forloop.counter0`从0计的循环次数、`forloop.first`是否第一次循环、`forloop.last`是否最后一次循环

## 其他

```html
<!-- 包含 -->
(% include "nav.html" %)
```

# Model

Model类是对数据库的封装，View通过调用Model进行数据库操作。通常设计为：每个模型类对应数据库的一张表，每个实例对应表中的一行数据，类的各属性对应表的各字段

```python
from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    votes = models.IntegerField(default=0)
```

将模型类写在`<app_name>/models.py`中，将应用添加到`settings.py`的`INSTALLED_APPS`中，并通过以下命令建表

```powershell
python manage.py makemigrations <app_name>
python manage.py migrate
```

第一步生成迁移（migration）命令，也就是实际建表的各种指令；第二步执行这些命令。数据库不在版本管理范围内，保留迁移命令等于保留了数据库结构。数据库通过名为`django_migrations`的表记录哪些迁移已经实施

```python
from django.utils import timezone

# 增
q = Question(question_text="What's new?", pub_date=timezone.now(), votes=0)
q.save()
q = Question.objects.create(question_text='idk', pub_date=timezone.now())

# 删

# 改
q0.votes = q0.votes + 1  # q0是一条已有的记录
q0.save()

# 查
q1 = Question.objects.all()
q2 = Question.objects.filter(question_text__startswith='What')
q3 = q2.exclude(pub_date__gte=datetime(2020, 1, 1))  # 用上一次查询结果继续查询，称作链式查询
entry = Question.objects.get(pk=1)    # 检索单一对象
```

查询的基本格式是`field__lookuptype = value`，字段名 双下划线 查询方式 = 值。常用的查询方式有

| 查询方式             | 说明                           |
| -------------------- | ------------------------------ |
| exact, contains      | 精确匹配，包含匹配             |
| startswith, endswith | 以什么开头或结尾               |
| gt, gte, lt, lte     | 大于、大于等于、小于、小于等于 |
| in                   | 包含于列表                     |

在查询方式前加上`i`不区分大小写。比如`name__istartswith = rick`可以匹配到`Rick Astley`

# 其他

## 静态文件

```python
# 在settings.py中声明静态文件夹
STATIC_URL = 'static/'     # 静态文件的url，必须斜杠结尾

STATICFILES_DIRS = [       # 静态文件夹。必须用UNIX格式
    BASE_DIR / "static",
    BASE_DIR / 'myapp/static',
]
```

并且在模板需要使用静态标签

```html
{% load static %}
<img src="{% static 'myapp/example.png' %}" />
```

如果是生产环境，官方文档建议另外弄一个服务器专门负责图片
