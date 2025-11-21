### Yak-Lang

缝合了各种语法糖的语言，自带丰富的网络、安全相关功能

```javascript
// 字符串
name = "John" + `Doe`
println("id=%d,name=%v" % [1, name])
println(f"Hello, ${name}")
sprintf("{%d, %v}", 1, name)
nums = x"id={{int(1-10)}}"  // x-string，展开fuzztag生成一个列表

// 列表与字典
arr = [1, 2, 3]
arr.Append(4)
user = {"name": "John", "age": 42}

// 控制流
// 支持python风格for-in，golang风格for-range和C风格的三段式写法
for user in users {
    if user["age"] > 18 {
        user["category"] = "Adult"
    } else if user["age"] > 0 {
        user["category"] = "Child"
    }
}
for (i=0; i<10; i++) {
    dump(i)
}

// 函数
myFunc = func() {    // 声明函数变量
    println("Hello World")
}
func myFunction() {  // “正常”函数定义。也可用def关键字定义
    println("Hello World")
}
myFunction = () => { // 箭头函数
    println("Hello World")
}
```

库函数速查：

- 打印：`println`打印换行；`dump`打印变量信息；`desc`打印结构体信息
- [文档](https://yaklang.com/docs/yak-basic/cap7-buildin-functions)

### 