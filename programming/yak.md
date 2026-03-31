缝合了各种语法糖的语言，自带丰富的网络、安全相关功能

缝的很多，因此一件事有很多种写法

# 语法基础

## 变量

所有变量都是动态类型，类似于Javascript

```javascript
// 定义变量
var a      // 定义。此时变量值为nil
var b = 1  // 定义并赋值
c := 2     // 定义并赋值，等同于var c = 2
d = 3      // 隐式定义
```

### 字符串

```javascript
// 可以用双引号、反引号。双引号会转义\n等字符，反引号不会
name = "John\n" + `Doe`

// 字符串格式化
println("id=%d,name=%v" % [1, name])  // 百分号格式化字符串
sprintf("{%d, %v}", 1, name)          // sprintf格式化
println(f"Hello, ${name}")            // f-string格式化
nums = x"id={{int(1-10)}}"            // x-string，展开fuzztag生成一个列表
```

### 列表和字典

```javascript
// 列表
arr = [1, 2, 3]
arr.Append(4)

// 字典
user = {"name": "John", "age": 42}
```

## 控制流

### 分支

```javascript
// if-elif，或者elif换成else if也可以
if score > 80 {
    team_score += 3
} elif score > 60 {
    team_score += 2
} else {
    team_score += 1
}
```

### 循环

```javascript
scores = [10, 20, 30, 40, 50, 60, 70, 80, 99, 100]

// python风格for-in
for score in scores {
    println(score)
}

// C风格三段式写法
for (i=0; i<10; i++) {
    dump(i)
}

// golang风格for-range
for index, user = range users {
    println(index, user["name"])
}
```

## 函数

```javascript
// 定义函数。func关键字可以替换成fn、def
func increment(i) {
    return i + 1
}

// 箭头函数
hello_func = () => {
    println("Hello World")
}
```

库函数速查：

- 打印：`println`打印换行；`dump`打印变量信息；`desc`打印结构体信息
- [文档](https://yaklang.com/docs/yak-basic/cap7-buildin-functions)

## 错误处理

```javascript
// 手动捕获、抛出错误
results, err = servicescan.Scan(scanTarget, scanPorts)
die(err)

// 使用WavyCall（`~`）捕获错误并抛出
results = servicescan.Scan(scanTarget, scanPorts)~

// 使用try-catch捕捉错误
try {
    results = servicescan.Scan(scanTarget, scanPorts)
} catch err {
    println(err)
}

// golang风格的defer-recover错误处理
func myFunc() {
    defer func {  // 
        err = recover()
        if err != nil {
            println(err)
        }
    }
    1 / 0
}
```



# 示例

本节记录解决问题的一些小脚本，之后再整理进知识库

```javascript
// RSA加密
decode2 = func(plaintext) {
    publicKey64 = `MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCseQUWale/2v7NqoqOPlO4AonSWI25ZYjnrmGzBk39QRd+Wp4TMq39kbekdK4qEzrFybasw9BhwyshIyEeMmIdzS7za/Fp1jHVXQLhT8A0sfZLx3t/HYFgVwNakOGeuh65dxQdpA/kUuhZsv7HCeSvSRRqiAA+lJXH6HuaDG3taQIDAQAB`
    encrypted = codec.RSAEncryptWithPKCS1v15(publicKey64, plaintext)~
    enc_b64 = codec.EncodeBase64(encrypted)
    enc_url = codec.EscapeQueryUrl(enc_b64)
    return enc_url
}

// AES加密
decode = func(plaintext) {
    
}
```

