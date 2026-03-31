---
title: infinite_blog
date: 2025-08-17 09:13:00
tags: []
mathjax: true
---

# LWE学习
## 1.Background
二十年来，格约化算法在破解密码系统方面的成功，确立了格约化作为公钥密码分析中最流行工具的地位。事实上，格在密码学中的应用长期以来主要是“负面的”。有趣的是，在许多实验中，LLL
及其他格约化算法的实际表现远好于最坏情况分析所保证的效果，这导致人们普遍认为“格约化在实践中是容易的”。

然而，对于 带噪声学习问题（Learning With Errors,
LWE），格约化算法的能力是有限的。当格的维度或误差足够大，或者给出的基被人为放大/混淆时，基约化将无法再找到格中的最短向量。这正是
LWE 被认为是一个“困难”问题、适合作为密码学基础的直观原因。

好的，我来翻译成中文（保持学术化、流畅的表述）：

## 2.Introduction
带噪声学习问题（Learning With Errors, LWE）
指的是这样一个计算问题：我们希望学习一个定义在某个环上的线性函数 $f(A)$，但是只能获得该函数的带噪声样本。这些样本通常形如：

$(A,\;\langle A, S \rangle +
e),$

其中：

- $S$
是定义该线性函数的秘密元素；
- $e$
是从某个已知分布中抽取的小噪声项；
- $A$ 是环中的已知元素；
- $\langle A, S \rangle$ 表示矩阵
$A$ 与向量 $S$ 的乘积。
### 基于 LWE
的密码系统通常具有以下共同特征：
1. 模运算：使用两个不同的模数——明文模数与密文模数。
2. 密钥结构：秘密密钥是一个模 $n$ 的向量空间中的元素。
3. 加密过程：通过将一个带噪声编码的消息加到一个大点积上来完成。
- 其中，带噪声的消息是明文与一个小噪声项的正确编码和。
- 点积部分是秘密密钥与某个随机向量的内积，这个随机向量作为密文的一部分提供。
因此，密文看起来像：

$(A,\;\langle A, S \rangle +
\text{encoded}(m, e)),$

其中 $A$ 是向量空间中的元素。

如果秘密密钥 $S$
已知，那么点积部分 $\langle
A,S\rangle$
可以被减去，剩下的就是带编码的消息与噪声。由于编码方式的特殊设计，噪声可以被去除，从而恢复出明文。

### LWE
中存储消息与噪声的两种常见方法：
- 高位存储消息：噪声放在低位。例如
Regev09、BFV。
- 低位存储消息：噪声放在高位。例如
BGV。
### 问题
如果没有加入噪声，那么消息可以通过多项式时间内的什么算法，从这些线性方程中恢复出来？

👉 答案：如果没有噪声，问题就退化为一个
线性方程组求解，因此可以使用
高斯消元法（Gaussian Elimination）
在多项式时间内恢复消息。

## 3.LWE High Bits Message
现在我们要解密一条 隐藏在高位的玩具 LWE
系统中的消息。

### 参数设置
- 向量空间维度：$n$
- 密文模数：$q$
- 明文模数：$p$（只能加密消息
$m < p$）
- 缩放因子： $$
Δ=\text{round}\!\left(\frac{q}{p}\right)
$$
### 密钥生成（Key-gen）
秘密密钥 $S$ 是向量空间 $\mathbb{Z}_q^n$ 中的一个随机元素。

### 密文格式
密文由一对 $(A, b)$
组成，其中：

- $A \in \mathbb{Z}_q^n$，
- $b \in \mathbb{Z}_q$。
### 加密过程（Encrypting message $m$）
1. 采样 $A$，它是向量空间 $\mathbb{Z}_q^n$ 的一个随机元素。
2. 采样误差项 $e$，它是范围 $$
[-\frac{\Delta}{2},\; \frac{\Delta}{2}\Bigr]
$$
内的整数。（注：实际系统里常用离散高斯分布，但这里用均匀分布即可。）
3. 计算： $$
b=⟨A,S⟩+Δ⋅m+e
$$
4. 输出密文对 $(A, b)$。
### 解密过程（Decrypting
ciphertext $(A, b)$）
1. 计算： $$
x=(b−⟨A,S⟩) mod q
$$ 并将结果解释为一个整数（不是模 $q$
的剩余类，而是落在对称区间的整数）。
2. 计算： $$
m = \text{round}\!\left(\frac{x}{\Delta}\right)
$$ 其中除法与取整均在整数域中完成。
3. 输出明文 $m$。
### 原理说明
在该系统中，解密能够正确进行的原因是：在去除掩码 $\langle A, S \rangle$
之后，剩余的部分满足：

$x = \Delta \cdot m + e,$

这个等式在整数域中成立，因此不会因模数 $q$
而产生“绕回”（wraparound）。这样，通过对整数商进行四舍五入，就可以去除误差项
$e$，恢复出明文 $m$。

为了保证解密正确，参数必须满足：

$\Delta \cdot m + e <
\frac{q}{2}.$

注意到在整数域完成，不然会出错！！！

```
from math import floor
from sage.all import *
from Crypto.Util.number import *
# dimension
n = 64
# plaintext modulus
p = 257
# ciphertext modulus
q = 0x10001
# bound for error term
error_bound = int(floor((q/p)/2))
# message scaling factor
delta = int(round(q/p))

V = VectorSpace(GF(q), n)
S = V.random_element()
print("S = ", S, "\n")

m = 20000
A = V.random_element()
error = randint(-error_bound, error_bound)
A = vector(Zmod(q),A)
S = vector(Zmod(q),S)
def encrypt(m):
    assert delta*m + error < q /2
    b = A*S + m*delta + error
    return (A,b)
def decrypt(A,b,S):
    x = round(int((b - A* S) % q)/delta)
    return x
```

## 4.LWE Low Bits Message
现在我们要直接跳到一个练习：解密一条隐藏在 LWE
系统低位中的消息。在这个系统中，噪声被存放在高位。

### 参数设置
- 向量空间维度：$n$
- 密文模数：$q$
- 明文模数：$p$（只能加密消息 $m < p$）
- 要求：$q$ 与 $p$ 互素
### 密钥生成（Key-gen）
秘密密钥 $S$ 是向量空间 $\mathbb{Z}_q^n$ 中的一个随机元素。

### 密文格式
密文由一对 $(A, b)$
组成，其中：

- $A \in \mathbb{Z}_q^n$
- $b \in \mathbb{Z}_q$
### 加密过程（Encrypting message
$m$）
1. 采样 $A$，它是向量空间 $\mathbb{Z}_q^n$ 的一个随机元素。
2. 采样误差项 $e$，它是范围 $$
[ \frac{q/p}{2}\Bigr]
$$
内的整数。（注：实际系统里通常从离散高斯分布采样，但这里用均匀分布即可。）
3. 计算 $$
b=⟨A,S⟩+m+p⋅eb = \langle A, S \rangle + m + p \cdot e
$$
4. 输出密文对 $(A, b)$。
### 解密过程（Decrypting
ciphertext $(A, b)$）
1. 计算 $$
x=b−⟨A,S⟩
$$ 并对其进行 中心化模约简（centered modulo）模
$q$，结果要落在区间 $$
(−q/2,  q/2]
$$ （不同于普通模约简的 $[0,
q-1]$ 区间）。
2. 将 $x$
解释为一个整数。
3. 计算 $$
m=x \quad  mod p
$$ （在整数域上进行除法与取余）。
4. 输出消息 $m$。
### 原理说明
在该系统中，解密之所以能够正确执行，是因为在去除了掩码 $\langle A, S \rangle$
之后，剩余的部分满足：

$x = m + p \cdot e,$

这个等式在整数域中成立，不会因为模 $q$
而发生“绕回”（wraparound）。因此，通过再对 $p$ 取模，就可以去除误差项 $e$，得到明文 $m$。

这要求参数选择必须满足：

$m + p \cdot e <
\frac{q}{2}.$

## 5.Publickey
这可以利用 LWE
的“可加同态”性质构造一个公钥密码系统。也就是说，给定一个密文 $\langle A, b \rangle$（它加密了消息 $m$），任何人都可以将其转化为一个合法的密文，从而加密
$m + m_2$。具体做法是：

- 对于低位消息（高位噪声存储），计算 $\langle A, b + m_2 \rangle$。
- 对于高位消息（低位噪声存储），计算 $\langle A, b + \Delta \cdot m_2
\rangle$。
这种可加同态性质在消息存储在低位时更直观，但即使消息存储在高位时也同样存在。

类似地，将两个 LWE
密文相加，会产生一个新的合法密文，它加密的是对应明文的和。密钥拥有者可以利用这一性质，把
LWE 变成一个公钥加密系统：

- 公钥中发布许多不同的“零的加密”。
- Alice
要加密时，先随机选择其中一些“零的加密”并把它们加起来。根据第二个可加同态性质，这仍然是零的一个合法加密。
- 接着，Alice 创建对她的消息 $m$
的编码，并将它加到上面这个零的密文中。根据第一个可加同态性质，这就是
$m$ 的一个合法加密。
要使该过程正确，噪声的分布必须仔细选择，以保证最终的误差项在解密所需阈值以下（高概率成立）。

为了保证安全性，攻击者必须难以判定到底是哪一些公钥样本被相加生成了最终的
LWE 密文。为此，公钥中的“零的加密”数目必须远大于 LWE 的维度。因此，LWE
公钥的大小按位复杂度为 $$
O(n^2 \log q)
$$ 这导致 LWE 加密系统的公钥通常非常庞大。

问题： Kyber1024 的公钥大小是多少字节？

## 6.no noise
### pwntools介绍
远程连接

```
io = remote(url,port)
```

接收数据

recv(n) - 接收任意数量的可用字节

recvline() - 接收数据直到遇到换行符

recvuntil(delim) - 接收数据直到找到分隔符

recvregex(pattern) - 接收数据直到满足正则表达式模式

recvrepeat(timeout) - 继续接收数据，直到发生超时

clean() - 丢弃所有缓冲数据发送数据

发送（数据） - 发送数据

sendline(line) - 发送数据加上换行