# case语句

case ... esac 与其他语言中的 switch ... case 语句类似，是一种多分枝选择结构。

语法格式

```shell
case 值 in
模式1)
    command1
    command2
    command3
    ;;
模式2）
    command1
    command2
    command3
    ;;
*)
    command1
    command2
    command3
    ;;
esac
```

实例

```shell
#!/bin/bash

echo "输入1-4数字"
echo -e "输入的数字是:\c"
read num
case $num in
        1) echo "选择1"
        ;;
        2) echo "选择2"
        ;;
        3) echo "选择3"
        ;;
        4) echo "选择4"
        ;;
        *) echo "不是1-4"
        ;;
esac
```

结果

```
输入1-4数字
输入的数字是:3
选择3
```

