[toc]

# Go语言环境搭建

## 下载地址

Go官网下载地址：https://golang.org/dl/

Go官方镜像站（推荐）：https://golang.google.cn/dl/

Windows下傻瓜安装，一直next

## 检查

检查是否安装成功

命令行里输入

```shell
go version
```

如果出现版本信息，则安装成功

## GOPATH配置

go工程的路径，比如`D:\go`

![image-20200818201620645](C:\Users\vt\AppData\Roaming\Typora\typora-user-images\image-20200818201620645.png)

在path中添加`D:\go\bin`

![image-20200818201855972](C:\Users\vt\AppData\Roaming\Typora\typora-user-images\image-20200818201855972.png)

### 检查

命令行中输入

```shell
go env
```

![image-20200818202046334](C:\Users\vt\AppData\Roaming\Typora\typora-user-images\image-20200818202046334.png)



## go 目录结构

### 通用目录结构

源代码都放在gopath src目录下，可以按照下面方式组织代码

![image-20200818202621574](C:\Users\vt\AppData\Roaming\Typora\typora-user-images\image-20200818202621574.png)

### 流行的目录结构

![image-20200818203319628](C:\Users\vt\AppData\Roaming\Typora\typora-user-images\image-20200818203319628.png)

### 企业目录结构

![image-20200818203518206](C:\Users\vt\AppData\Roaming\Typora\typora-user-images\image-20200818203518206.png)

## go开发编辑器

傻瓜式安装`goland`

配置gopath 和 goroot