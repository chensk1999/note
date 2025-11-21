# Web服务器

Web服务器负责接受HTTP请求，并返回HTTP响应；处理静态请求，并作为反向代理将动态请求转发给应用服务器；还常用于负载均衡、SSL终止

## Apache

### 指纹特征



### 常见漏洞

**多后缀解析漏洞**

Apache支持一个文件拥有多个后缀（参考：[mod_mime](https://httpd.apache.org/docs/current/mod/mod_mime.html)），比如使用以下配置，访问`index.cn.html`返回中文页面

```htaccess
AddType text/html .html
AddLanguage zh-CN .cn
```

假如配置不当，如`AddHandler application/x-httpd-php .php`，那么服务器会认为`evil.php.jpg`这样“不是php”的文件也包含后缀`.php`，并当作php解析。较新版本（应该是PHP 7+）的php配置文件（`php<版本号>.conf`）默认使用如下配置，不会产生多后缀解析漏洞

```htaccess
<FilesMatch ".+.php$">
    SetHandler application/x-httpd-php
</FilesMatch>
```

**换行解析漏洞**（CVE-2017-15715）：Apache 2.4.0-2.4.29版本，访问`evil.php\x0A`，即`evil.php\n`，按照php文件解析

### 其他

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

## Nginx

### 指纹特征



### 常见漏洞

**自动修复路径漏洞**

若配置Nginx的`cgi.fix_pathinfo=1`，cgi解析出错时会匹配上一级文件，比如`http://example.com/evil.jpg/non-exist.php`，这个文件不存在，就会尝试把`evil.jpg`交给PHP-FPM（这个配置的原意是修复`PATH_INFO`错误）；若同时配置PHP-FPM的`security.limit_extensions=空`，则PHP-FPM可以解析任意后缀的文件，因此将`evil.jpg`作为php解析

很久以前（应该是php 5.3）PHP-FPM的默认配置就改为了`security.limit_extensions = .php`，Nginx的默认配置也禁用了`cgi.fix_pathinfo`

**文件名逻辑漏洞**（CVE-2013-4547）

Nginx 0.8.41~1.4.3 / 1.5.0~1.5.7，若文件名包含`\x20\x00`就无法正确检测`\x00`

上传文件`evil.jpg\x20`，访问`evil.jpg\x20\x00.php`，Nginx没有正确识别到`\x00`，认为它是正常php文件并发送给PHP-FPM；PHP-FPM读取文件名时被00截断，读取`evil.jpg\x20`。若同时配置了`security.limit_extensions=空`则会将`evil.jpg\x20`作为php解析

## IIS

### 指纹特征



### 常见漏洞

**目录解析漏洞**：IIS 5.x / 6.0版本中，名为`*.asp, *.asa, *.cer, *.cdx`的目录中所有文件都解析为asp文件

**文件名解析漏洞**：IIS 5.x / 6.0版本中，`evil.asp;.jpg`解析为asp文件

**畸形解析漏洞**：IIS 7.0版本，与Nginx自动修复路径漏洞类似，开启Fast-CGI模式且`cgi.fix_pathinfo=1`，访问`evil.jpg/non-exist.php`，会将`evil.jpg`作为php文件解析

## OpenResty



# 应用服务器

应用服务器负责运行动态代码（如JSP、ASPX、PHP），处理业务逻辑、数据库交互。它独立于Web服务器运行，处理由Web服务器转发来的动态请求。应用服务器也可以不依赖Web服务器，直接处理用户的请求，但其处理静态请求的性能远不如Web服务器

### Tomcat

**PUT方法任意写入文件**（CVE-2017-12615）

Tomcat 8.5.19，若配置`readonly=false`，使用PUT方法就能上传任意文件。Tomcat会做后缀黑名单校验，可以用`shell.jsp/`等方式绕过

### Weblogic

### JBoss / WildFly

# 框架

开发框架提供开发规范（如MVC），并封装ORM、权限认证等常用功能。开发完成之后编译或打包，部署到应用服务器

## Java

### Spring Boot

Spring Boot架设在Spring框架之上，通过增加中间层的方式简化了Spring框架的配置，是目前使用Spring开发的主流手段

指纹特征

- 绿色树叶图标![SpringBoot favicon.ico](data:image/x-icon;base64,AAABAAEAEA0AAAEAIACcAwAAFgAAACgAAAAQAAAAGgAAAAEAIAAAAAAAdAMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAZqBwHEaPV4xCq4dWQcq6T0LNv2I7z8R7NtDGkjPQxaQszsSkMtDGoDvSyHlI08otAAAABAAAAAAAAAAAAAAAADeaazIvgUL7K306/yqFSP8olGH/JqR9/yS5of8jxbX/Is3D/yLNwv8hzMH/Js3C/zHPxZ5B0skYAAAAAETSxyUuwa3PJqmF/yelfv4onnP/KZZm/yqPWP8rhUf/KpBa/yawkf8jyr3/Is7E/iLMwf8izMH/MM/FpwAAAAY00MafIc3D/yLQx/4i0Mj/ItHJ/yLQyP8jyr3/JL2o/yaphv8qk1//KJxw/yTEtP8iz8X+IszB/yTNwv9A0slGMM/F3CLMwf8jzcL/I83C/yPMwf8izcL/Is3C/yLOxP8izsX/JMSy/yeqhv8onnL/JMOy/yLOxP4izMH/M9DGrDDPxcoizMH/I83C/yPNwv8jzcL/I83C/yPNwv8jzMH/Is3C/yLNwv8jzMH/Jbaa/yesiv8jyLr/Is3C/y/Pxek60chyIszB/yLNwv8jzcL/I83C/yPNwv8jzcL/I83C/yPNwv8jzcL/I8zB/yLOxf8mtZr/JcCs/yLNwv8ozcP/AAAACC3OxNEjzcL/IszB/yLMwf8izMH/IszB/yLMwf8izMH/IszB/yLMwf4jzMH/Is7E/yXAq/8jyr3+Jc3D/wAAAABW1s4aLc7EribNwuUmzcL4JM3C/SXNwv4lzcL7Jc3C+iXNwv8jzcL/IszB/yLNwv8jy7/+IszB/yrOxPwAAAAAAAAAAAAAAAA+0sg/Mc/FbCrOxHgtz8V5L8/FcyzPxHEvz8SBLM/EoynOw9ckzcL/Is3C/yLMwf8uz8TkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAU50ccsMs/FdijOw+sizMH/MtDFuwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJA0sgyJ83D5zjRx4QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAELSyThP1c04gAcAAIABAAAAAQAAAAAAAAAAAAAAAAAAAAAAAIAAAACAAAAA4AAAAP/gAAD/+AAA//wAAA==)，FOFA语法：`icon_hash="116323821"`
- 错误页面`White Label Error Page`

常见漏洞

- 敏感信息泄露：Spring Boot提供`actuator`模块，用于监控系统状态。1.5以下默认允许未授权访问所有端点，≥1.5则默认只能访问`/actuator/health`和`/actuator/info`端点。端点详情参考[对于Spring Boot的渗透姿势](https://blog.zgsec.cn/archives/129.html)
- 扫描工具：[SpringBoot-Scan](https://github.com/AabyssZG/SpringBoot-Scan)，Burp插件[SpringScan](https://github.com/metaStor/SpringScan)

## PHP

### Yii

**指纹特征**：橙绿蓝图标：![Yii_favicon](data:image/x-icon;base64,AAABAAEAEBAQAAEABAAoAQAAFgAAACgAAAAQAAAAIAAAAAEABAAAAAAAgAAAAAAAAAAAAAAAEAAAAAAAAADwlEMAAAAAAALJcwAAjP8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAERERERERERERERAAAAEREREREAAAAREREREQAAABERERERAAAAEREREREAAAAREREREQAAABEREREREREREREREREREREREREzMzMRIiIiETMzMxEiIiIRMzMzESIiIhEzMzMRIiIiETMzMxEiIiIRMzMzESIiIhERERERERERH//wAA+B8AAPgfAAD4HwAA+B8AAPgfAAD4HwAA//8AAP//AACBgQAAgYEAAIGBAACBgQAAgYEAAIGBAAD//wAA)、![Yii_icon](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABT0lEQVR42pXRA4xmMQAE4L6zbdu2bUsxTtE50i+cvYzWtm0pXNu2re6s+0uTfPHMe22JLvkWcX0iTCHKUic8OROWw2KYrKS8Bv6AGayRL++FYMiBVLCDWzB1pDwfPIGO+A0cO3AO2oAyWuA7fX54+tfI6/dR6GIGEmERO7AS0oDK6Wnin+T9DLv+erDIKIDV8sd4B51AWfWCk1XhJuc/4S8qmYF4mCs/MB0+QDb0sCOV0lNu+IswZkCo6iU4WA2PwRjSG4QnehoEJ8os3S874y8GyymwkWhKn3A/Vyw8v9JF9PJ/seBSXoTpOf8vkdcrUH5ItM1SccLB5eL49CsixxR7w2eWPyKvPsfARK3Kq8Uxc8EL6CpxLN0qDflN68gEom1QfAJdQAEjMW90KXNgBnRECqzXZWAmRAOFHLhGEF0H/sJn2KFLlz3CFOCIhgwAOLEWj9GPpGYAAAAASUVORK5CYII=)

**常见弱点**

### ThinkPHP

### Laravel

### RuoYi

## 前端

# 中间件&组件

中间件通常是提供特定服务的独立进程，与其他组件通过TCP/IP协议进行通信；其他组件则直接运行在应用服务器（或者其他中间件）上

## Druid

## Shiro

[Shiro](https://greycode.github.io/shiro/doc/introduction.html)是一个开源Java安全框架，提供身份认证、访问控制、会话管理等功能。Shiro通过Servlet Filter集成到Web应用中，收到请求时首先交给Shiro进行身份认证，若认证未通过，进行相应处理，例如跳转到登录页、返回401；若认证通过则交给下一个Servlet处理

**指纹特征**：Shiro默认使用Servlet容器的会话管理，即用`JSESSIONID`标识会话；其自动登录功能使用名为`rememberMe`的Cookie。若数据包Cookie带有`rememberMe`字段，或者在请求包添加`rememberMe`字段后，响应包设置Cookie`rememberMe = deleteMe`，可判定使用了Shiro

**常见弱点**：参考[Shiro漏洞研究](https://github.com/HackJava/Shiro)

## FastJson

FastJson是阿里巴巴开发的JSON序列化、反序列化库，它使用方便而且运行速度快，因此很受欢迎。但其历史版本出现过若干严重的反序列化漏洞

**指纹特征**：待补充

**常见弱点**：参考[FastJson漏洞研究](https://github.com/HackJava/Fastjson)

## Log4j2

Log4j2是Apache开源的Java日志库，它也是Log4j的升级版

**指纹特征**：待补充

**常见弱点**：待补充

# 设备

## 路由器

## 安全设备

飞塔防火墙：Fortinet / FortiGate

路径：`https://example.com:9680/remote/login`

默认密码：`admin / 空`

DrayTek：Vigor-3900

## 物联网

# 其他

Message HTTP Binding Service：应该是.Net框架的WCF接口，可能是SOAP API，也可能充当网关，接收外部SOAP请求并转发到内部真实服务

Webpack
