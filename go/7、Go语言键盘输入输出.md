# 键盘输入和输出

## 打印输出

- fmt.Print

  直接打印

- fmt.Printf

  格式化打印

  常见格式化打印换行符

  ```
  %v,原样输出
  %T，打印类型
  %t,bool类型
  %s，字符串
  %f，浮点
  %d，10进制的整数
  %b，2进制的整数
  %o，8进制
  %x，%X，16进制
  %x：0-9，a-f
  %X：0-9，A-F
  %c，打印字符
  %p，打印地址
  ```

- fmt.Println

  打印后换行

示例

```go
package main

import "fmt"

func main() {
	a := 3.14
	fmt.Print(a,"\n")

	b := 100
	c := 3.14
	d := true
	e := "haha"
	f := 'A'
	fmt.Printf("%T, %d\n", b, b)
	fmt.Printf("%T, %f\n", c, c)
	fmt.Printf("%T, %t\n", d, d)
	fmt.Printf("%T, %s\n", e, e)
	fmt.Printf("%T, %c, %d\n", f, f, f)
	fmt.Printf("%v", f)

}
```

结果

```
3.14
int, 100
float64, 3.140000
bool, true
string, haha
int32, A, 65
65
```

## 键盘输入

- fmt.Scan
- fmt.Scanf
- fmt.Scanln
- bufio包读取

示例

```go
var g int
fmt.Println("输入一个整数")
fmt.Scan(&g)
fmt.Printf("g的值为:%d\n", g)

var i int
var j float64
fmt.Println("输入一个整数,一个浮点数")
fmt.Scanf("%d,%f", &i, &j)
fmt.Printf("i:%d,j:%f\n", i , j)

var k int
var m float64
fmt.Println("输入一个整数,一个浮点数")
fmt.Scanln(&k, &m)
fmt.Printf("k:%d,m:%f\n", k , m)
```

结果

```
输入一个整数
20
g的值为:20
输入一个整数,一个浮点数
100,3.25
i:100,j:3.250000
输入一个整数,一个浮点数
100
k:100,m:0.000000
```

示例

```go
fmt.Println("请输入一个字符串：")
reader := bufio.NewReader(os.Stdin)
s1 , _ := reader.ReadString('\n')
fmt.Println("读到的数据为:", s1)
```

结果

```
请输入一个字符串：
hello
读到的数据为: hello
```

