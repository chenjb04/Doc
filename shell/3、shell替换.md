[toc]

# shell替换

### 转义字符

如果表达式中包含特殊字符，Shell 将会进行替换。例如，在双引号中使用变量就是一种替换，转义字符也是一种替换。

```shell
#!/bin/bash
a=10
echo -e "value is $a\n"
```

结果

```shell
value is 10

```

如果不加 -e，是不会转义的 ，会原样输出

常用的转义字符

| 转义字符 | 含义                             |
| -------- | -------------------------------- |
| \\       | 反斜杠                           |
| \a       | 警报，响铃                       |
| \b       | 退格（删除键）                   |
| \f       | 换页(FF)，将当前位置移到下页开头 |
| \n       | 换行                             |
| \r       | 回车                             |
| \t       | 水平制表符（tab键）              |
| \v       | 垂直制表符                       |

### 命令替换

命令替换是指Shell可以先执行命令，将输出结果暂时保存，在适当的地方输出。

语法(两个反引号包含命令)

```shell
`command`
```

实例

```shell
#!/bin/bash
date=`date`
echo "date is $date"
```

结果

```shell
date is Thu Jul 23 11:08:46 CST 2020
```

### 变量替换

量替换可以根据变量的状态（是否为空、是否定义等）来改变它的值。

变量替换形式

| 形式            | 说明                                                         |
| --------------- | ------------------------------------------------------------ |
| ${var}          | 变量本来的值                                                 |
| ${var:-word}    | 如果变量 var 为空或已被删除(unset)，那么返回 word，但不改变 var 的值。 |
| ${var:=word}    | 如果变量 var 为空或已被删除(unset)，那么返回 word，并将 var 的值设置为 word。 |
| ${var:?message} | 如果变量 var 为空或已被删除(unset)，那么将消息 message 送到标准错误输出，可以用来检测变量 var 是否可以被正常赋值。 若此替换出现在Shell脚本中，那么脚本将停止运行。 |
| ${var:+word}    | 如果变量 var 被定义，那么返回 word，但不改变 var 的值。      |

实例

```shell
#!/bin/bash
echo ${var:-"var is not set"}
echo "1- value var is ${var}"

echo ${var:="var is not set"}
echo "2 - value var is ${var}"

unset var
echo ${var:+"This is default value"}
echo "3 - value of var is $var"

var="haha"
echo ${var:+"This is default value"}
echo "4 - value of var is $var"

echo ${var:?"Print this message"}
echo "5 - value of var is ${var}"
```

结果

```shell
var is not set
1- value var is 
var is not set
2 - value var is var is not set

3 - value of var is 
This is default value
4 - value of var is haha
haha
5 - value of var is haha
```

