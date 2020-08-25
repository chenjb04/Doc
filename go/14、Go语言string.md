# Go语言string

## 概念

Go中的字符串是一个字节的切片。可以通过将其内容封装在“”中来创建字符串。Go中的字符串是Unicode兼容的，并且是UTF-8编码的。

## string操作

### 初始化

可以使用`""`或者``反引号

示例

```go
s1 := "hello"
s2 := `hello world`
fmt.Println(s1) // hello
fmt.Println(s2) // hello world
```

### 访问字符串

可以通过下标来访问

```go
fmt.Println(s1[0])  // 104
fmt.Printf("%c", s1[0])  // h
```

### 遍历字符串

字符串也有索引，可以使用range

```go
for i := 0; i < len(s1); i++ {
    fmt.Printf("%c\t", s1[i])  //h	e	l	l	o
}
fmt.Println()
for i, v := range s1 {
    fmt.Printf("%d ", i)
    fmt.Printf("%c\n", v)
}

/*
h	e	l	l	o	
0 h
1 e
2 l
3 l
4 o
*/
```

### 字符串和字节转换

字符串是字节的集合，可以相互转换

示例

```go
slice1 := []byte{65, 66, 67, 68, 69}
s3 := string(slice1)
fmt.Println(s3)  // ABCDE

s4 := "ABCDE"
slice2 := []byte(s4)
fmt.Println(slice2) //[65 66 67 68 69]
```

## strings包

访问strings包，可以有很多操作string的函数。

## strconv包

访问strconv包，可以实现string和其他数值类型之间的转换。