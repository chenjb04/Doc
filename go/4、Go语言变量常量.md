# Go语言变量

## 概念

变量是为存储特定类型的值而提供给内存位置的名称。在go中声明变量有多种语法。

所以变量的本质就是一小块内存，用于存储数据，在程序运行过程中数值可以改变

## 声明变量

### 定义变量

- var声明单个变量

  指定变量类型，声明后若不赋值，使用默认值

  语法格式

  ```
  var 变量 数据类型
  变量名 = 赋值
  
  var 变量 数据类型 = 赋值
  ```

  示例

  ```go
  var num int
  num = 50
  //或者写在一行
  var num2 int = 30
  ```

- 类型推断

  根据值自行推断变量类型

  如果一个变量有一个初始值，Go将自动能够使用初始值来推断该变量的类型。因此，如果变量具有初始值，则可以省略变量声明中的类型

  语法格式

  ```
  var 变量名 = 赋值
  ```

  示例

  ```go
  var name = "小明"
  fmt.Printf("name 的类型是%T, 值是：%s\n", name, name)  // name 的类型是string, 值是：小明
  ```

- 简短声明

  省略var, 注意 :=左侧的变量不应该是已经声明过的(多个变量同时声明时，至少保证一个是新变量)，否则会导致编译错误(简短声明)

  语法格式

  ```
  变量名 := 赋值
  ```

  示例

  ```go
  num3 := 50
  ```

### 声明多个变量

- 以逗号分隔，声明与赋值分开，若不赋值，存在默认值

  语法格式

  ```
  var name1, name2, name3 type
  name1, name2, name3 = v1, v2, v3
  ```

  示例

  ```go
  var a1, a2, a3 int
  a1 = 10 
  a2 = 20
  a3 = 30
  fmt.Printf("a1:%d,a2: %d,a3:%d\n", a1, a2, a3) //a1:10,a2: 20,a3:30
  ```

- 直接赋值，下面的变量类型可以是不同的类型(类型推断)

  语法格式

  ```
  var name1, name2, name3 = v1, v2, v3
  ```

  示例

  ```go
  var b1, b2, b3 = "haha", 20, 123
  fmt.Printf("b1:%s, b2:%d,b3:%d", b1, b2, b3) //b1:haha, b2:20,b3:123
  ```

- 集合类型

  语法格式

  ```
  var (
      name1 type1
      name2 type2
  )
  ```

  示例

  ```go
  var (
      studentName = "小明"
      age = 17
  )
  fmt.Printf("学生：%s，年龄：%d\n", studentName, age) //学生：小明，年龄：17
  ```

## 注意事项

- 变量必须先定义才能使用
- go语言是静态语言，要求变量的类型和赋值的类型必须一致。
- 变量名不能冲突。(同一个作用于域内不能冲突)
- 简短定义方式，左边的变量名至少有一个是新的
- 简短定义方式，不能定义全局变量。
- 变量的零值。也叫默认值。
- 变量定义了就要使用，否则无法通过编译。

# Go语言常量

## 概念

常量是一个简单值的标识符，在程序运行时，不会被修改的量

## 常量声明

语法格式

```
const identifier [type] = value
```

```
显式类型定义： const b string = "abc"
隐式类型定义： const b = "abc"
```

常量组可以作为枚举类型使用

```go
// 常量组
const (
Unknown = 0
Female = 1
Male = 2
)
fmt.Println(Unknown)
fmt.Println(Female)
fmt.Println(Male)
```

常量组中如不指定类型和初始化值，则与上一行非空常量右值相同

```go
const (
    A = 1
    B
    C = "haha"
    D
	)
fmt.Println(A) // 1
fmt.Println(B) // 1
fmt.Println(C) // haha 
fmt.Println(D) // haha
```

## 注意事项

- 常量中的数据类型只可以是布尔型、数字型（整数型、浮点型和复数）和字符串型
- 不曾使用的常量，在编译的时候，是不会报错的
- 显示指定类型的时候，必须确保常量左右值类型一致，需要时可做显示类型转换。这与变量就不一样了，变量是可以是不同的类型值

## iota

iota，特殊常量，可以认为是一个可以被编译器修改的常量

第一个 iota 等于 0，每当 iota 在新的一行被使用时，它的值都会自动加 1

在出现下一组常量时iota清零

```go
const (
    a = iota
    b = iota
    c = iota
)
fmt.Println(a) // 0
fmt.Println(b) // 1
fmt.Println(c) // 2

// 新常量 清零
const (
    d = iota
) 
fmt.Println(d) // 0

// 枚举
const (
    Unknown = iota
    Female
    Male
)
fmt.Println(Unknown, Female, Male) // 0 1 2

const (
    a1 = iota   //0
    b1          //1
    c1          //2
    d1 = "ha"   //独立值，iota += 1
    e1          //"ha"   iota += 1
    f1 = 100    //iota +=1
    g1          //100  iota +=1
    h1 = iota   //7,恢复计数
    i1          //8
)
fmt.Println(a1,b1,c1,d1,e1,f1,g1,h1,i1) // 0 1 2 ha ha 100 100 7 8
```

