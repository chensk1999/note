# 服务器&框架

## Apache

```yaml
/etc/<包名>/:    # 配置文件。包名可能是apache, apache2, httpd, nginx等
    - <包名>.conf        # 主配置文件
    - ports.conf         # 监听端口配置
    - sites-enabled/     # 虚拟主机配置
    - mods-enabled/      # 模块配置
    - conf-enabled/      # 其他配置

/var/www/:
    - html/              # 网站默认根目录

/var/log/<包名>/:
    - access.log         # 访问日志
    - access_log
    - error.log          # 错误日志
    - error_log
```

# 读文章

怎么做笔记：

1. 漏洞产生点：什么功能有可能出现此漏洞，要尽量具体，比如登录框，又比如绑定微信
2. 漏洞类型：可以归类到哪个类型。新漏洞基本也是经典类型的变种，可以帮助梳理成体系
3. 利用方法：怎么构造载荷
4. 遇到问题：常规做法受阻之后怎么办



[src漏洞挖掘 支付漏洞四舍五入](https://mp.weixin.qq.com/s/9VSyzXf6O8tKGOFw9ZjYKQ)

- 产生点：充值、提现、转账
- 类型：逻辑漏洞 - 金额舍入误差
- 利用方法：提现带小数金额，查看账户余额变动与银行卡余额变动是否匹配
- 遇到问题：找类似业务的功能点进行测试

> 举一反三：整数参数都有可能有四舍五入导致的漏洞，比如手机号：13511112222和13511112222.1可能被当作不同手机号导致短信轰炸；比如资源id：有权访问`id=1`，无权访问`id=2`，尝试`id=1.9`有可能越权

[一次并发高危投稿](https://mp.weixin.qq.com/s/XwJxFXNzeBdd78hINrnoLg)

- 产生点：关注、取关
- 类型：条件竞争漏洞
- 利用方法：多并发请求包
- 遇到问题：找相似功能点

> 举一反三：限制操作次数的功能并发通常都有较大危害，比如领券、抽奖、新用户优惠

[某src支付逻辑有误导致任意支付](https://mp.weixin.qq.com/s/SSgQf547szihmhjgr5AiJQ)

- 产生点：余额付款
- 类型：逻辑漏洞 - 后端未校验
- 利用方法：篡改返回包让余额大于订单金额，欺骗前端暴露支付接口，再修改支付数据包的支付模式
- 遇到问题：抓全部数据包改可疑参数

[基于 cookie 的 XSS](https://mp.weixin.qq.com/s/N45buKTkzB_gKHb5YLKVtQ?scene=1)

- 产生点：网页显示Cookie的值
- 类型：XSS
- 利用方法：在可控子域部署恶意页面，该页面将载荷写入根域Cookie，再重定向到目标页面。XSS执行JS更改页面显示登录界面，诱骗受害者输入登录凭据
- 遇到问题：通过利用子域名的漏洞将本地XSS变成远程XSS；“正牌”Cookie优先级比子域名设置的Cookie高，因此对已登录用户来说此漏洞无危害，于是转而逆向JS，让页面显示登录界面，诱骗未登录用户输入账号密码

# 思路

挖洞的目的：证明目标服务器不安全：权限、数据、破坏。除了传统漏洞外，也要从这三个角度思考有没有利用点

1. 筛选出比较常见通用的、危害比较高影响比较大的漏洞点
2. 以漏洞利用结果相同或相似为条件进行分类
3. 头脑风暴， 将所有可能实现目标的攻击途径列举出来，不断在实战中进行尝试利用

常见功能的思路

- 登录：弱口令；验证码可爆破/复用；短信轰炸

# 认证

## 相关名词

信息安全中，权限指用户操作资源（增删查改）的权力。系统使用凭证（密码，短信验证码，Session，JWT等）鉴别用户是否拥有权限。正常情况下拥有凭证 ≈ 拥有权限。但是，当权限控制失效时，这个约等于号就要换成不等于号了

- 认证（Authentication）：验证用户身份。通常是验证用户拥有的凭证（密码、短信验证码等）
- 授权（Authorization）：下发服务器使用的凭证（Session，JWT，Access Token等），允许用户操作资源
- 鉴权：用户试图进行操作时，判断凭证是否有效、操作是否在用户权限范围内

## OAuth 2.0

https://www.ruanyifeng.com/blog/2014/05/oauth_2_0.html

- 用户，也叫资源所有者，通过用户代理访问服务
- 资源服务器，也叫第三方应用、客户端（Client）
- 认证服务器

**授权码（Authorization Code）模式**

1. 用户访问资源服务器，后者将前者导向认证服务器
2. 用户给予授权，认证服务器将用户导回资源服务器，同时下发授权码给用户
3. 用户访问资源服务器，并将授权码也发出去。资源服务器收到授权码，向认证服务器申请令牌。这一步在资源的服务器上完成，对用户不可见
4. 认证服务器核对授权码，确认无误后，向资源服务器发送访问令牌（access token）和更新令牌（refresh token）

**简化（Implicit）模式**

1. 客户端将用户导向认证服务器
2. 用户决定是否给于客户端授权
3. 假设用户给予授权，认证服务器将用户导向客户端指定的"重定向URI"，并在URI的Hash部分包含了访问令牌
4. 浏览器向资源服务器发出请求，其中不包括上一步收到的Hash值
5. 资源服务器返回一个网页，其中包含的代码可以获取Hash值中的令牌
6. 浏览器执行上一步获得的脚本，提取出令牌
7. 浏览器将令牌发给客户端

## JWT

https://www.ruanyifeng.com/blog/2018/07/json_web_token-tutorial.html

JWT（JSON Web Token）的原理是将会话信息存储在客户端。其结构是`Header . Payload . Signature`，其中Header和Payload是base64编码的JSON字符串，分别描述了此Token的元数据、数据；Signature是对前面数据的签名

通常放在Authorization字段或Cookie中传递

## Cookie与Authorization

身份凭据可以存储在Cookie，也可以存储在localStorage中

- CSRF：Cookie有CSRF风险，需要设置`SameSite`属性或使用CSRF Token；Authorization无CSRF风险
- XSS：Cookie设置HttpOnly后不会被XSS窃取；Authorization很容易窃取
- 跨域：Cookie跨域麻烦，Authorization跨域简单；对于微服务这样的跨域架构很重要

注：也可以用Authorization以外的随便什么请求头

有状态与无状态 - Session，Cookie与Token

localStorage与sessionStorage

# 其他

Host碰撞

若服务器配置了只能通过域名访问，“关闭”服务器时仅仅解除了域名解析，没有真正关掉服务器，我们收集到历史域名就能尝试通过此域名访问服务器。历史域名和IP往往不匹配，很可能要在大量候选IP中碰撞出真正的地址
