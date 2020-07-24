# grep

grep命令是一种强大的文本搜索工具，它能使用正则表达式搜索文本，并把匹 配的行打印出来

### 语法格式

```shell
grep [OPTION] file..
```

### 参数选项

- -i：忽略大小写
- -c:统计匹配到字符串的次数
- -n:顺便输出行号
- -v:反向选择，显示没有匹配到的内容
- -o：只显示匹配到的串
- -A:显示匹配到的字符后面的n行
- -B:显示匹配到的字符前面的n行
- -C:显示前后各n行

### 示例

```shell
 grep echo *.sh  # 从所有以sh结尾的文件中搜索echo字符串
 
 grep echo 1.sh 2.sh # 从1.sh和2.sh的文件中搜索echo字符串
 
 grep -v echo 1.sh  # 输出除了echo之外行的所有行
 
 grep echo 10.sh --color=auto # 颜色高亮
 
 grep -o -n  echo 10.sh # 输出只匹配到的和行号
 
 grep -E [a-b]+ 10.sh # 使用正则表达式
 grep -c echo 10.sh #统计匹配到字符串的行数
```

