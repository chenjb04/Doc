# 循环

### for循环

语法格式

```shell
for 变量 in 列表
do
    command1
    command2
    ...
    commandN
done
```

实例

```shell
#!/bin/bash

for loop in 1 2 3 4 5 6
do
    echo "value is: ${loop}"
done

for str in "i love you"
do
    echo "${str}"
done

for file in $PWD/*.sh
do
    echo "${file}"

done
```

结果

```
value is: 1
value is: 2
value is: 3
value is: 4
value is: 5
value is: 6
i love you
/home/shell/10.sh
/home/shell/11.sh
/home/shell/1__.sh
```

### while 循环

语法格式

```shell
while command
do
   do something
done
```

实例

```shell
#!/bin/bash


count=0
while [ $count -lt 10 ]
do
   echo "$(($count * $count))"
   count=`expr ${count} + 1`
done
```

### until 循环

until 循环执行一系列命令直至条件为 true 时停止。until 循环与 while 循环在处理方式上刚好相反。

实例

```shell
#!/bin/bash
x=0
until [ $x -ge 5 ]
do
   echo $x
   x=`expr $x + 1`
done
```

结果

```
0
1
2
3
4
```

### select循环

和for循环语法差不多，有些许区别

select循环语句由如下特点：

- select语句使用Bash内部变量PS3的值作为它的提示符信息。

- 打印到屏幕上的列表LIST中的每一项都会加上一个数字编号。

- 当用户输入的数字和某一个数字编号一致时，列表中响应的项即被赋予变量VAR。

- 如果用户输入为空，将重新显示列表LIST中的项和提示符信息。

- 可以通过添加一个退出选项，或者Ctrl+C、Ctrl+D组合键退出select循环。

实例

```shell
#!/bin/bash

PS3="Run command:"
clear
select choice in date w hostname "uname -r" Exit
do
case $choice in
    date)
    $choice
    ;;
    w)
    $choice
    ;;
    "uname -r")
    $choice 
    ;;  
    hostname)
    $choice
    ;;
    Exit)
    echo "Bye!"
    exit 0
    ;;
esac
done
```

```
1) date
2) w
3) hostname
4) uname -r
5) Exit
Run command:1
Fri Jul 24 11:32:49 CST 2020
Run command:2
 11:32:53 up 52 days,  1:48,  1 user,  load average: 5.76, 5.69, 5.53
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
root     pts/0    1.190.237.79     10:37    5.00s 13.54s  0.00s w
Run command:3
VM_0_5_centos
Run command:4
3.10.0-957.21.3.el7.x86_64
Run command:5
Bye!
```

### 跳出循环

如果想提前结束一个循环或跳过某次循环执行，可以使用 shell 的`break`和`continue`语句来实现。它们可以在任何循环中使用。

#### break

用来提前结束当前循环

实例

```shell
#!/bin/bash
# 求10以内的第一个偶数
x=0
while [ $x -lt 10 ]
do
    if [ `expr $x % 2` == 0 ]
    then
        echo $x
        break
   fi
   x=`expr $x + 1`
done 
```

结果

```
0
```

#### continue

用来跳过某次迭代

实例

```shell
#!/bin/bash
NUMS="1 2 3 4 5 6 7"
for NUM in $NUMS
do
   Q=`expr $NUM % 2`
   if [ $Q -eq 0 ]
   then
      echo "Number is an even number!!"
      continue
   fi
   echo "Found odd number"
done
```

结果

```
Found odd number
Number is an even number!!
Found odd number
Number is an even number!!
Found odd number
Number is an even number!!
Found odd number
```



