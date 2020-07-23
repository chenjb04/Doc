[toc]

# 变量

shell中没有数据类型，无需提前声明变量，给变量赋值会直接创建变量。

### 变量命名规则

- 命名只能使用英文字母，数字和下划线，首个字符不能以数字开头。
- 中间不能有空格，可以使用下划线（_）。
- 不能使用标点符号。
- 不能使用 bash里的关键字。

### 定义变量

```shell
var_name="hello"
name="xiaoming"
```

**变量名和等号之间不能有空格。**

### 使用变量

使用一个定义过的变量，只要在变量名前面加美元符号（$）即可

```shell
name="xiaoming"
echo ${name}
```

变量名外面的花括号是可选的，加不加都行，加花括号是为了帮助解释器识别变量的边界，所以推荐加花括号。

### 只读变量

使用 readonly 命令可以将变量定义为只读变量，只读变量的值不能被改变。

```shell
rworld="xiaoming"
echo ${rworld} # xiaoming
readonly rworld
rworld="xiaoli" # 报错 -bash: rworld: readonly variable
```

### 删除变量

使用 unset 命令可以删除变量。变量被删除后不能再次使用。unset 命令不能删除只读变量。

```shell
unset name # 删除成功
unset rworld # 删除失败 -bash: unset: rworld: cannot unset: readonly variable
```

### 变量类型

运行shell时，会同时存在三种变量：

- 局部变量

  ```
  局部变量在脚本或命令中定义，仅在当前shell实例中有效，其他shell启动的程序不能访问局部变量。
  ```

- 环境变量

  ```
  所有的程序，包括shell启动的程序，都能访问环境变量，有些程序需要环境变量来保证其正常运行。必要的时候shell脚本也可以定义环境变量。
  ```

- shell变量

  ```
  shell变量是由shell程序设置的特殊变量。shell变量中有一部分是环境变量，有一部分是局部变量，这些变量保证了shell的正常运行
  ```

### 特殊变量

变量名只能包含数字、字母和下划线，因为某些包含其他字符的变量有特殊含义，这样的变量被称为**特殊变量**

| 变量 | 含义                                                         |
| ---- | ------------------------------------------------------------ |
| $0   | 当前脚本的文件名                                             |
| $n   | 递给脚本或函数的参数。n 是一个数字，表示第几个参数。例如，第一个参数是`$1`，第二个参数是`$2` |
| $#   | 传递给脚本或函数的参数个数。                                 |
| $*   | 传递给脚本或函数的所有参数。                                 |
| $@   | 传递给脚本或函数的所有参数。被双引号(" ")包含时，与 `$*` 稍有不同 |
| $?   | 上个命令的退出状态，或函数的返回值。                         |
| $$   | 当前Shell进程ID。对于 Shell 脚本，就是这些脚本所在的进程ID。 |

实例

```shell
#!/bin/bash
echo "文件名字：$0"
echo "第一个参数为：$1"
echo "第二个参数为：$2"
echo "总共有 $# 个参数"
echo "参数为：$*"
echo "参数为：$@"
echo "退出状态: $?"
echo "进程id：$$"
```

结果

```shell
文件名字：spec_var.sh
第一个参数为：hello
第二个参数为：world
总共有 3 个参数
参数为：hello world nihao
参数为：hello world nihao
退出状态: 0
进程id：19985
```

#### $*和$@的区别

$* 和 $@ 都表示传递给函数或脚本的所有参数，不被双引号(" ")包含时，都以"$1" "$2" … "$n" 的形式输出所有参数。

但是当它们被双引号(" ")包含时，"$*" 会将所有的参数作为一个整体，以"$1 $2 … $n"的形式输出所有参数；"$@" 会将各个参数分开，以"$1" "$2" … "$n" 的形式输出所有参数。

实例

```shell
#!/bin/bash
echo "\$*=" $*
echo "\"\$*\"=" "$*"
echo "\$@=" $@
echo "\"\$@\"=" "$@"
echo "print each param from \$*"
for var in $*
do
    echo "$var"
done
echo "print each param from \$@"
for var in $@
do
    echo "$var"
done
echo "print each param from \"\$*\""
for var in "$*"
do
    echo "$var"
done
echo "print each param from \"\$@\""
for var in "$@"
do
    echo "$var"
done
```

执行 `./test.sh "a" "b" "c" "d"`，看到下面的结果

```shell
$*=  a b c d
"$*"= a b c d
$@=  a b c d
"$@"= a b c d
print each param from $*
a
b
c
d
print each param from $@
a
b
c
d
print each param from "$*"
a b c d
print each param from "$@"
a
b
c
d
```

#### 退出状态

`$?` 可以获取上一个命令的退出状态。所谓退出状态，就是上一个命令执行后的返回结果

退出状态是一个数字，一般情况下，大部分命令执行成功会返回 0，失败返回 1。

不过，也有一些命令返回其他值，表示不同类型的错误。