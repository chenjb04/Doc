# 循环语句

for循环是唯一的循环语句，go没有while循环

语法

```
for init; condition; post {}
```

初始化语句只执行一次。在初始化循环之后，将检查该条件。如果条件计算为true，那么{}中的循环体将被执行，然后是post语句。post语句将在循环的每次成功迭代之后执行。在执行post语句之后，该条件将被重新检查。如果它是正确的，循环将继续执行，否则循环终止。

示例

```go
func main() {
	// 打印5次hello world
	for i := 1; i <= 5; i++ {
		fmt.Println("hello,world")
	}
}
```

## for 循环变体

组成的三个部分，都是可选的

可以省略其一，或者都省略

示例

相当于Python中的`while 条件表达式`语句

```go
j := 1
for j <=5 {
    fmt.Println(j)
    j++
}
```

相当于Python中的`while True`

```go
for {
		fmt.Println("hello,world")
	}
```

## break

break：跳出循环体。break语句用于在结束其正常执行之前突然终止for循环

```go
for i := 1; i <= 5; i++ {
    if i == 3 {
        break
    }
    fmt.Println(i)
}

/*
1
2
*/
```

## continue

continue：跳出一次循环。continue语句用于跳过for循环的当前迭代。在continue语句后面的for循环中的所有代码将不会在当前迭代中执行。循环将继续到下一个迭代。

示例

```go
for i := 1; i <= 5; i++ {
    if i == 3 {
        continue
    }
    fmt.Println(i)
}
/*
1
2
4
5
*/
```

## goto

可以无条件地转移到过程中指定的行。

语法

```
goto label;
..
..
label: statement;
```

示例

```go
a := 10
for a < 20 {
    if a == 15 {
        a++
        goto GOTOLABEL

    }
    fmt.Println("a", a)
    a++
}
GOTOLABEL:
fmt.Println("done")

/*
a 10
a 11
a 12
a 13
a 14
done
*/
```

