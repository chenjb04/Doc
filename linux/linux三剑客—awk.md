# linux三剑客—awk

## 概念

AWK是一种处理文本文件的语言，是一个强大的文本分析工具。特点是处理灵活，功能强大。可实现统计、制表以及其他功能。

## 格式

```shell
awk [options] 'command' file
awk -f script-file file
```

## 命令格式

`awk [-F|-f|-v] ‘BEGIN{} //{command1; command2} END{}’ file`

- [-F|-f|-v]   大参数，-F指定分隔符，-f调用脚本，-v定义变量 var=value
- BEGIN   初始化代码块，在对每一行进行处理之前，初始化代码，主要是引用全局变量，设置FS分隔符
- //           匹配代码块，可以是字符串或正则表达式
- {}           命令代码块，包含一条或多条命令
- ；          多条命令使用分号分隔
- END      结尾代码块，在对每一行进行处理之后再执行的代码块，主要是进行最终计算或输出结尾摘要信息

## 内置参数

- 1，$2...           表示整个当前行
- $1          每行第一个字段
- NF          字段数量变量
- NR          每行的记录号，多文件记录递增
- FILENAME    文件名

## 示例

数据准备

```shell
cp /etc/passwd ./
```

### $1..

```shell
awk -F ':' '{print "name:" $1"\t""uid:" $3}' passwd
# name:root       uid:0
# name:bin        uid:1
# name:daemon     uid:2
```

###  NR，NF，FILENAME

```shell
awk -F ':' '{print "line:" NR, "col:" NF,"name:" FILENAME}' passwd
# line:1 col:7 name:passwd
# line:2 col:7 name:passwd
```

### if

```shell
awk -F ':' '{if ($3 > 100) printf ("line:%3s col:%s user:%s\n", NR,NF, $1)}' passwd
# line: 14 col:7 user:systemd-network
# line: 16 col:7 user:polkitd
```

### 配合正则表达式使用

```shell
awk -F ':' '/^a/{print $1}' passwd
# adm
# abrt
```

### begin  end

```shell
awk -F ':' 'BEGIN{print "line col user"}{print NR " | "  NF " | "  $1}END{print "-----------"FILENAME}' passwd 
# line col user
# 1 | 7 | root
# 2 | 7 | bin
# 3 | 7 | daemon

# 统计文件大小
ll | awk 'BEGIN{size=0}{size+=$5}END{print "size is " size/1024/1024"M"}'

# 统计不为空的行数
 awk -F ':' 'BEGIN{count=0}$1!~/^$/{count++}END{print "count=" count}' passwd
```

### 计算平均成绩和总成绩

test1

```
zhangsan 80
lisi 81.5
wangwu 93
haha 78
zhangsan 82
lisi 90
wangwu 99
haha 95
```

```shell
awk 'BEGIN{print "name  |  avg  |  total"}{score[$1]+=$2;count[$1]+=1}END{for (i in score) print i, score[i]/count[i], score[i]}' test1

# name  |  avg  |  total
# zhangsan 81 162
# wangwu 96 192
# haha 86.5 173
# lisi 85.75 171.5
```

