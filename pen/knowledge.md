# 数据库

## MySQL

# 路径

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

## api

| 路径               | 说明                              |
| ------------------ | --------------------------------- |
| `/swagger`         | Swagger UI 默认文档访问路径       |
| `/swagger-ui.html` | Spring Boot 集成 Swagger 常见路径 |
| `/swagger-ui/`     | Swagger UI 静态资源路径           |
| `/api-docs`        | OpenAPI JSON/YAML 文档路径        |
| `/v2/api-docs`     | Swagger 2 默认文档路径            |
| `/openapi.json`    | OpenAPI 规范 JSON 格式文档        |
| `/openapi.yaml`    | OpenAPI 规范 YAML 格式文档        |
| `/docs`            | 一般通用的文档路径                |
| `/api/docs`        | 一般通用的接口文档路径            |
| `/redoc`           | Redoc 生成的 API 文档路径         |

# 其他

php的`md5('ffifdyop', true)`前几个字节恰好是`'or'6`（后面的就是乱码了），因此可以用作SQL注入。不过很难想象有网站使用这么古怪又不安全的摘要，估计也就CTF比赛可能考

