# 条件语句

## if语句

语法格式

```
if 条件表达式 {
 do something
}
```

```
if 条件表达式 {
 do something
} else {
do something
}
```

```
if 条件表达式 {
 do something
} else if {
do something
} else {
 do something
}
```

示例

```go
func main() {
	var score int
	fmt.Println("输入成绩分数:")
	fmt.Scanln(&score)
	if  score >= 90 {
		fmt.Println("成绩优秀", score)
	} else if score >= 60 && score < 90  {
		fmt.Println("成绩良好", score)
 	} else {
 		fmt.Println("成绩不及格", score)
	}
}
```

if 变体

```
if statement; condition {  
}

```

示例

```go
if num := 4;num > 5 {
	fmt.Println("数比5大", num)
} else {
	fmt.Println("数比5小", num)
}
```

## switch语句

语法格式

```
switch var1 {
    case val1:
        ...
    case val2:
        ...
    default:
        ...
}
```

如果switch没有表达式，它会匹配true

Go里面switch默认相当于每个case最后带有break，匹配成功后不会自动向下执行其他case，而是跳出整个switch, 但是可以使用fallthrough强制执行后面的case代码。

变量 var1 可以是任何类型，而 val1 和 val2 则可以是同类型的任意值。类型不被局限于常量或整数，但必须是相同的类型；或者最终结果为相同类型的表达式。 您可以**同时测试多个可能符合条件的值，使用逗号分割它们**，例如：case val1, val2, val3。

示例

```go
package main

import "fmt"

func main() {
	var score int
	fmt.Println("请输入分数")
	fmt.Scanln(&score)

	switch score {
	case 60:
		fmt.Println("及格")
	case 80:
		fmt.Println("良好")
	case 90:
		fmt.Println("优秀")
	default:
		fmt.Println("其他")
	}

	switch {
	case  score >= 90:
		fmt.Println("成绩优秀", score)
	case score >= 60 && score < 90:
		fmt.Println("成绩良好", score)
	case score < 60:
		fmt.Println("不及格", score)
	default:
		fmt.Println("其他", score)
	}
	letter := 'A'
	switch letter {
	case 'A', 'E', 'I', 'O', 'U':
		fmt.Println("元音")
	case 'M','N':
		fmt.Println("M or N")
	default:
		fmt.Println("其他")

	}

}

```

