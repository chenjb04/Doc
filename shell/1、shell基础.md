[toc]

# shell解释器

### shell常见解释器

- sh：sh 是 Unix 标准默认的 shell
- bash： bash 是 Linux 标准默认的 shell
- fish：智能和用户友好的命令行 shell
- xiki：使 shell 控制台更友好，更强大
- zsh：功能强大的 shell 与脚本语言

### 指定脚本解释器

在 shell 脚本，`#!` 告诉系统其后路径所指定的程序即是解释此脚本文件的 Shell 解释器。`#!` 被称作shebang（也称为 Hashbang ）

- 指定sh解释器

  ```shell
  #!/bin/sh
  ```

- 指定bash解释器

  ```shell
  #!/bin/bash
  ```

### 执行shell脚本

- sh\bash执行

  ```shell
  sh test.sh
  bash test.sh
  ```

- 工作目录执行

  ```shell
  chmod +x test.sh
  ./test.sh
  ```

  

# 基本语法

### 注释

- 单行注释

  ```
  以 # 开头，到行尾结束
  ```

- 多行注释

  ```
  以 :<<EOF 开头，到 EOF 结束
  ```

示例

```shell
#! /bin/bash
echo "hello world"
# echo "单行注释"
:<<!
echo "多行注释"
echo "多行注释1"
!
```

结果

```shell
hello world
```

### 打印输出

#### echo

echo 用于字符串的输出。

输出普通字符串

```shell
echo "hello world"
```

输出含有变量的字符串

```shell
name=haha
echo "${name}"
```

输出含有换行符的字符串

```shell
echo -e "yes\nno"  # -e 开启转义
```

输出字符串重定向到文件中

```shell
echo "hello" > test
```

输出执行结果

```shell
echo `pwd`
```

#### printf

printf 用于格式化输出字符串。

默认，printf 不会像 echo 一样自动添加换行符，如果需要换行可以手动添加 `\n`。

```shell
# 单引号
printf '%d %s\n' 1 "hello"
# 1 hello

# 双引号
printf "%d %s\n" 1 "hello"
# 1 hello

# 无引号
printf hello
# hello 不会换行

# 格式只指定了一个参数，但多出的参数仍然会按照该格式输出
printf "%s\n" "hello" "world"
# hello
# world

#如果没有参数，那么 %s 用 NULL 代替，%d 用 0 代替
printf "%s and %d \n"
# and 0
```

