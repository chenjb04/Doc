# Go语言Map

## 概念

map是Go中的内置类型，它将一个值与一个键关联起来。可以使用相应的键检索值。

Map 是一种无序的键值对的集合。Map 最重要的一点是通过 key 来快速检索数据，key 类似于索引，指向数据的值 Map 是一种集合，所以我们可以像迭代数组和切片那样迭代它。不过，Map 是无序的，我们无法决定它的返回顺序，这是因为 Map 是使用 hash 表来实现的，也是引用类型

使用map过程中需要注意的几点：

- map是无序的，每次打印出来的map都会不一样，它不能通过index获取，而必须通过key获取
- map的长度是不固定的，也就是和slice一样，也是一种引用类型
- 内置的len函数同样适用于map，返回map拥有的key的数量
- map的key可以是所有可比较的类型，如布尔型、整数型、浮点型、复杂型、字符串型……也可以键。

## 初始化map

```
var 变量名 map[key类型] 值类型
var 变量名 map[key类型] 值类型{k:v...}
var 变量名 = make(map[key类型] 值类型)
```

如果不初始化 map，那么就会创建一个 nil map。nil map 不能用来存放键值对

示例

```go
var map1 map[string]int
var map2 = make(map[string]int)
var map3 = map[string]int{"Go": 100, "python": 100, "Java": 100}
fmt.Println(map1)  // map[]
fmt.Println(map2)  // map[]
fmt.Println(map3) //map[Go:100 Java:100 python:100]
```

## Map操作

### 添加或者修改数据

语法

```
map[key] = value
```

key 存在就是修改，key不存在就是添加

示例

```go
map2["A"] = 100
map2["B"] = 80
map2["C"] = 60
fmt.Println(map2) // map[A:100 B:80 C:60]

map2["B"] = 75
fmt.Println(map2) // map[A:100 B:75 C:60]
```

### 获取数据

```
map[key]
```

示例

```go
fmt.Println(map2["A"]) // 100
```

如果获取不存在的key数据时，会返回value类型的默认值

```go
fmt.Println(map2["D"]) // 0 获取不存在的key 是零值
```

还可以使用ok来确定返回的是默认值，还是map本身的值

```
value, ok := map[key]
```

示例

```go
val, ok := map2["E"]
if ok {
    fmt.Println("获取的是map值:", val)
} else{
    fmt.Println("获取的是零值")
}
```

### 删除

语法

```
delete(map, key)
```

示例

删除不存在的key，对map本身没有影响

```go
delete(map2, "C")
delete(map2, "D")
fmt.Println(map2) // map[A:100 B:75]
```

### 获取长度

len()函数可以获取map的键值对数量

示例

```go
fmt.Println(len(map2)) // 2
```

### map遍历

range遍历

```go
for k, v := range map2 {
    fmt.Println(k, v)
}
/*
A 100
B 75
*/
```

## map是引用类型

与切片相似，映射是引用类型。当将映射分配给一个新变量时，它们都指向相同的内部数据结构。因此，一个的变化会反映另一个

示例

```go
map4 := make(map[string]string)
map4["name"] = "xiaomi"
map4["address"] = "北京市"
map5 := map4
fmt.Println(map4) //map[address:北京市 name:xiaomi]
fmt.Println(map5) //map[address:北京市 name:xiaomi]

map5["name"] = "lisi"
fmt.Println(map4) //map[address:北京市 name:lisi]
fmt.Println(map5) //map[address:北京市 name:lisi]
```

