

```
/var/log/nginx/access.log
/var/log/apache/access.log
```



php的`md5('ffifdyop', true)`前几个字节恰好是`'or'6`（后面的就是乱码了），因此可以用作SQL注入。不过很难想象有网站使用这么古怪又不安全的摘要，估计也就CTF比赛可能考
