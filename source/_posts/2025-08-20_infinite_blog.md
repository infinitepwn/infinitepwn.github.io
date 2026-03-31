---
title: infinite_blog
date: 2025-08-20 10:44:37
tags: []
mathjax: true
---

# SQL注入
在ctf中，我们通常通过get请求和post请求，提交参数，然后服务器后端拼接sql代码，进行查询数据

```
$sql = "SELECT * FROM users WHERE username = '$username' AND password = '$password'";
```

比如说这里就是通过get请求提交username

我们后面都以这个为例

```
$sql = "SELECT * FROM users WHERE id = $id";
```

根据sql语句的不同，可以分为字符型和数字型

## 数字型
```
$sql = "SELECT * FROM users WHERE id = $id";
```

这种就是数字型

我们可以在后面加引号来测试

然后看爆错信息

## 字符型
```
$sql = "SELECT * FROM users WHERE id = '$id'";
```

You have an error in your SQL syntax; check the manual that
corresponds to your MariaDB server version for the right syntax to use
near ''1'' LIMIT 0,1' at line 1

比如根据这个爆错信息就可以知道

大概是

```
$sql = "SELECT * FROM sometable WHERE somecol = '$wllm' LIMIT 0,1";
```