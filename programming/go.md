# 基础

Go是Google开发的一种静态强类型、编译型、并发型，并具有垃圾回收功能的编程语言。它的并发性能较好，常用于服务器后端

Go语言的语法类似C

```go
package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}
```

https://www.runoob.com/go/go-structures.html

# 语法

## 变量

```go
// 声明变量。类型可以省略，省略时自动推断
var i int = 0
var s string = "Hello"

func f(){
    b := false   // 隐式声明变量。会自动推断类型。只能在函数内使用
}

// 常量
const LENGTH int = 10

// 数组与指针
var balance = [5]float32{1000.0, 2.0, 3.4, 7.0, 50.0}
var arr = [...]int{0, 1, 2, 3, 4}  // 自动判断长度
var pointer *int = &i
if pointer != nil {
    fnt.Printf("i = %d\n", *pointer)
}

// 切片。切片是对数组的引用，它可以实现变长数组
var slice []int = arr[0:3];
```

## 运算符

和C基本一致

## 控制流

和C基本一致，区别是条件不需括起来。以下记下不同之处

```go
strings := []string{"google", "runoob"}
for i, s := range strings {
    fmt.Println(i, s)
}
```

## 函数

```go
func swap(x, y string) (string, string) {
   return y, x
}
```

