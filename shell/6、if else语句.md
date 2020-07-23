# if else语句

### if else

语法

```shell
if [ expression ]
then
	do something
else
	do something
fi
```

如果 expression 返回 true，then 后边的语句将会被执行；如果返回 false，执行 else 后边的语句。

注意：

- 最后必须以 fi 来结尾闭合 if
- expression 和方括号([ ])之间必须有空格，否则会有语法错误

示例

```shell
#!/bin/bash
a=2
b=3
if [ $a == $b ]
then
        echo "a=b"
else
        echo "a!=b"
fi
```

结果

```
a!=b
```

### if elif 语句

语法

```shell
if [ expression 1 ]
then
	do something
elif [ expression 2 ]
then
	do something
else
	do something
fi
```

哪一个 expression 的值为 true，就执行哪个 expression 后面的语句

示例

```shell
#!/bin/bash
a=2
b=3
if [ $a == $b ]
then
        echo "a=b"
elif [ $a -gt $b ]
then
        echo "a>b"
elif [ $a -lt $b ]
then
        echo "a<b"
else
        echo "a!=b"
fi
```

结果

```
a<b
```

