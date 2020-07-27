# linux三剑客—sed

## 概念

sed是一种流编辑器，它是文本处理中非常重要的工具，能够完美的配合正则表达式使用，功能不同凡响。处理时，把当前处理的行存储在临时缓冲区中，称为“模式空间”（pattern space），接着用sed命令处理缓冲区中的内容，处理完成后，把缓冲区的内容送往屏幕。接着处理下一行，这样不断重复，直到文件末尾。文件内容并没有 改变，除非你使用重定向存储输出。Sed主要用来自动编辑一个或多个文件；简化对文件的反复操作；编写转换程序等。

## 语法格式

```shell
sed [选项参数] ‘command’ filename
```

## 选项参数

- -n 安静模式，仅显示script处理后的结果，不再默认显示模式空间中的内容
-  -e 多点编辑
-   -f /PATH/SCRIPT_FILE: 从指定文件中读取编辑脚本
-   -r 支持使用扩展正则表达式
-   -i 直接编辑原文件

## command

- d: 删除符合条件的行
- p：显示符号条件的行
- a：在当前行下面插入文本
- i：在当前行上面插入文本
- c：把选定的行改为新的文本。
- n：读取下一个输入行，用下一个命令处理新的行而不是用第一个命令
- s: 替换指定字符
- q：退出
- r：从file中读行

## 示例

test文件包含以下内容

```shell
you are so good
you are so handsome
you really have the money
you are six six six
```



### p打印指定行

```shell
# 打印test文件第三行内容
sed -n '3p' test
# you really have the money

# 打印test文件2到4行内容
sed -n '2,4p' test 
# you are so handsome
# you really have the money
# you are six six six

# 正则表达式确定行
sed -n '/six/,/six/p' test
# you are six six six

# 不会选择1-3行内容
sed -n '1, 3!p' test
# you are six six six

# 间隔行 输出1、3、5...行
sed -n '1~2p' test
# you are so good
# you really have the money

```

### a下一行插入

```shell
# 在第一行下面插入***
sed -i '1a **********' test

# 在第二到第四行下插入
sed -i '2,4a **********' test
```

### i在上一行插入

```shell
# 在第一行上面插入#!/bin/bash
sed -i '1i #!/bin/bash' test
```

### c选定行改成指定文本

```shell
# 把第二行改成hahaha
sed -i '2c hahaha' test

# 把所有的*行改成 ----
sed -i '/\*/c ------------' test
```

### d删除行

```shell
# 删除第三行内容
sed -i '3d' test

```

### s替换命令

```shell
# 把 -替换成*
sed 's/-/*/' test

#把第三行的-替换成*
sed '3s/-/*/' test

# g 全局替换
sed '3s/-/*/g' test
```

### sed多个命令，用{}包住，用；隔开或者加-e

```shell
# 删除3-5行，把-替换成*
sed '{3,5d;s/-/*/g}' test
# 等价于
sed -e '3,5d' -e 's/-/*/g' test
```

### n读取下一个输入行

```shell
# 读取1,3,5,7 相当于sed -n '1~2p' test
sed -n '{p;n}' test
```

### r复制指定文件插入到匹配行 w复制匹配行到指定文件

```shell
# 把123内容复制到 test文件第一行下面 改变的是test文件
sed -i '1r 123.txt' test

# 把test的1到6行输出到234.txt 文件 改变的是234文件
sed -i '1,6w 234.txt' test
```



