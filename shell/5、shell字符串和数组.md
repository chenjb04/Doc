[toc]

# 字符串

### 单双引号

shell 字符串可以用单引号 `''`，也可以用双引号 `“”`，也可以不用引号。

- 单引号的特点
  - 单引号里不识别变量
  - 单引号里不能出现单独的单引号（使用转义符也不行），但可成对出现，作为字符串拼接使用。
- 双引号的特点
  - 双引号里识别变量
  - 双引号里可以出现转义字符

综上，推荐使用双引号。

### 拼接字符串

```shell
#!/bin/bash
name="haha"
# 使用单引号拼接
str1='hello, '$name''
str2='hello, ${name}'
echo $str1 
echo $str2

# 使用双引号拼接
str3="hello, "${name}""
str4="hello, ${name}"
echo $str3
echo $str4
```

结果

```shell
hello, haha
hello, ${name}
hello, haha
hello, haha
```

### 获取字符串长度

```shell
#!/bin/bash
str="hahaha"
echo ${#str}
```

结果

```
6
```

### 截取字符串

```shell
#!/bin/bash
str="i love you"
echo ${str:2:3} # 下标从0开始 从下标为2的索引开始 截取3个字符
```

结果

```
lov
```

### 查找子字符串

```shell
#!/bin/bash/

str="i love you"

echo `expr index "$str" l`
echo `expr index "$str" you` #最后一个参数是字符，会对后面字符串每一个单独查找，返回最靠前的index
echo `expr index "$str" o`
echo `expr length "$str"` #字符串长度
echo `expr substr "$str" 1 6` #从字符串中位置1开始截取6个字符。索引是从0开始的。
```

结果

```
3
4
4
10
i love
```

# 数组

bash支持一维数组（不支持多维数组），并且没有限定数组的大小。类似与C语言，数组元素的下标由0开始编号。获取数组中的元素要利用下标，下标可以是整数或算术表达式，其值应大于或等于0。

### 定义数组

```shell
array=(value1 value2 value3)
```

或者单独定义数组的各个分量

```shell
array[0]=value
array[1]=value1
array[2]=value2
```

可以不使用连续的下标，而且下标的范围没有限制。

### 访问数组

 格式${array_name[index]} index索引

实例

```shell
#!/bin/bash
array[0]=value
array[1]=value1
array[4]=value4
echo ${array[1]}
echo ${array[4]}
echo ${array[*]}
echo ${array[@]}
```

结果

```
value1
value4
value value1 value4
value value1 value4
```

 `${array[*]}`和 `${array[@]}`可以访问所有元素,但是有点区别，当被双引号(" ")包含时，"*" 会将所有的参数作为一个整体，“@”会将各个参数分开

实例

```shell
#!/bin/bash
array=(red yellow "blue dark")
printf "%s\n" "${array[@]}"
printf "%s\n" "${array[*]}"
```

结果

```
red
yellow
blue dark
red yellow blue dark
```

访问数组部分元素

```shell
#!/bin/bash
array=(red yellow green "blue dark")
echo ${array[@]:1:2} # 从索引为1开始 访问两个元素
```

结果

```
yellow green
```

### 获取数组长度

```shell
#!/bin/bash
array=(red yellow green "blue dark")
echo ${#array[*]}
echo ${#array[@]}
echo ${#array[1]}  # 获取单个元素长度
```

结果

```
4
4
6
```



