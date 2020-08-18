# 第一个go程序

在`D:\go\src\demo`下创建hello.go程序

```go
package main //声明main包，表明当前是一个可执行程序

import "fmt" //导入内置fmt包
func main() { // main函数，是程序执行的入口
    fmt.Println("hello world") //在终端打印 Hello World!
}
```

## 执行go程序

- go run 命令

  切换到`D:\go\src\demo`目录下，命令行执行

  ```
  go run hello.go
  ```

- go build命令

  在项目目录下生成可执行文件 

  切换到`D:\go\src\demo`目录下，命令行执行

  ```
  go build
  ```

  或者在任意目录下执行

  ```
  go build demo
  ```

  go编译器会去 `GOPATH`的src目录下查找你要编译的demo项目,编译得到的可执行文件会保存在执行编译命令的当前目录下.

  终端直接执行

  ```
  ./demo.exe
  ```

  我们还可以使用`-o`参数来指定编译后得到的可执行文件的名字。

  ```
  go build -o xxxx.exe
  ```

- go install命令

  在任意路径下执行

  ```
  go install demo
  ```

  或者

  切换到`D:\go\src\demo`目录下，命令行执行

  ```
  go install
  ```

  在编译生成go程序的时，go实际上会去两个地方找程序包： GOROOT下的src文件夹下，以及GOPATH下的src文件夹下。

  在程序包里，自动找main包的main函数作为程序入口，然后进行编译。

  运行go程序 在/go/bin/下(如果之前没有bin目录则会自动创建)，会发现出现了一个hello的可执行文件，用如下命令运行: ./hello

## 解释说明

### package 

- 在同一个包下面的文件属于同一个工程文件，不用`import`包，可以直接使用
- 在同一个包下面的所有文件的package名，都是一样的
- 在同一个包下面的文件`package`名都建议设为是该目录名，但也可以不是

### import

import "fmt" 告诉 Go 编译器这个程序需要使用 fmt 包的函数，fmt 包实现了格式化 IO（输入/输出）的函数

可以是相对路径也可以是绝对路径，推荐使用绝对路径（起始于工程根目录）

- 点操作

  ```go
  import (
  	. "fmt"
  )
  ```

  这个点操作的含义就是这个包导入之后在你调用这个包的函数时，你可以省略前缀的包名，也就是前面你调

  用的`fmt.Println("hello world")`可以省略的写成`Println("hello world")`

- 别名操作 

  ```go
  import(
  	f "fmt"
  ) 
  ```

  别名操作的话调用包函数时前缀变成了我们的前缀，即`f.Println("hello world")`

- _操作

  ```go
  import (
    "database/sql"
    _ "github.com/ziutek/mymysql/godrv"
  ) 
  ```

  _操作其实是引入该包，而不直接使用包里面的函数，而是调用了该包里面的init函数

### main

main函数是程序的入口



