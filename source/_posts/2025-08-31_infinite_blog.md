---
title: infinite_blog
date: 2025-08-31 08:18:39
tags: []
---

# CSP研究综述
image-20250901214517993着重听了Feng Hao教授的课程，Chenglu
Jin教授的有点偏硬件，没怎么听懂

由于我平常会做一些ctf中crypto的问题，所以研究比较偏向于“实现”

了解的比较多的会详细，了解的比较少的就略过了

## 4种普遍的攻击方式
1.Ciphertext-only attack

2.Known-plaintext attack

3.Chosen-plaintext attack

4.Chosen-ciphertext attack

## 1.古典密码
### 1.凯撒密码
加解密使用同一个算法，加密是确定性的，同一个明文用相同的密钥加密完后得到的密文是相同的
\[
E(m) = m + k \mod 26 \\
D(c) = c - k \mod 26
\]
那就可以使用词频攻击，不过凯撒密码的密钥空间非常小，也就是26，通常直接遍历密钥，寻找有意义的明文字符串就行

Python实现

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
import random
def Enc(key,plaintext:str):
    ciphertext = ''
    for i in plaintext:
        if i.isupper():
            ciphertext += chr(ord('A')+(ord(i)-ord('A')+key)%26)
        elif i.islower():
            ciphertext += chr(ord('a')+(ord(i)-ord('a')+key)%26)
        else:
            ciphertext += i
    return ciphertext
def Dec(key,ciphertext:str):
    return Enc(-key,ciphertext)
plain = "CSP_Course_Is_Good!"
key = random.randint(1,26)
cipher = Enc(key,plain)
print(cipher)
for i in range(26):
    print(Dec(i,cipher),i)
#CSP_Course_Is_Good! 20
```

在遍历中找到有意义的解密结果，于是发现密钥是20

### 2.Vigenère
Vigenère 密码是一种多表代换密码 \[
C_i = (P_i + K_i) \mod 26
\]

\[
P_i = (C_i - K_i) \mod 26
\]

这样的话，对于每个明文来说，其实还是凯撒密码，但是整体不是，由于相同的明文遇到的密钥可能不同，因此密文不会相同，比凯撒密码安全很多，曾被认为是不可攻破的

以山大英语简介为例，如果用密钥“vigenere”加密，密钥长度为8

加密过程都统一成小写

得到密文，这里都用图片了，不然有点水字数

image-20250829114458933#### 1.Kasiski检验
我们可以在这里面寻找重复的密文片段，

由于英语中the的出现概率很高，我们考虑，如果长度为3的两个密文相同的话，假设两个明文分别为
\[
p_{i}p_{i+1}p_{i+2} \\ p_{j}p_{j+1}p_{j+2}
\] 密钥长度为m，假设j>i,也就是说 \[
p_{i}+k_{i\mod m} \equiv p_{j}+k_{j\mod m} \mod 26 \\p_{i+1}+k_{i+1\mod
m} \equiv p_{j+1}+k_{j+1\mod m} \mod 26\\p_{i+2}+k_{i+2\mod m} \equiv
p_{j+2}+k_{j+2\mod m} \mod 26
\] 那么明文相等意味着 \[
k_{i\mod m} \equiv k_{j\mod m} \mod 26 \\k_{i+1\mod m} \equiv k_{j+1\mod
m} \mod 26\\k_{i+2\mod m} \equiv k_{j+2\mod m} \mod 26
\]
相等有两种情况，一种是刚好密钥中有重复的字符，或者是下标模相等

如果密钥足够随机的话，应该还是下标模相等的概率比较大

那么就有 \[
i-j =km
\] 多找几组i，j，求i-j的公因数，就能预测m

用正则表达式，寻找空格+三个字符+空格这种形式

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
import re
pattern = r' (.{3}) '
from collections import defaultdict
matches = defaultdict(list)

for m in re.finditer(pattern, cipher):
    p = m.group(1)
    pos = m.start(1)
    matches[p].append(pos)
for p, pos in matches.items():
    print(f"{p}: {pos}")
```

然后我们就可以求公因数了

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
for p, pos in matches.items():
    print(f"{p}: {pos}")
    if len(pos) > 1:
        km = [] 
        for i in range(len(pos)-1):
            km.append(pos[i+1]-pos[i])
        from itertools import combinations
        from Crypto.Util.number import *
        for a, b in combinations(km, 2):
            ms.append(GCD(a,b))
print(set(ms))
#{1, 2, 3, 4, 5, 67, 7, 8, 73, 41, 11, 12, 45, 50, 22, 31}
```

这意味着密钥长度有这些备选

可以看到密钥长度8确实在里面

不过还有更好用的

#### 2.重合指数攻击
简单思路就是给密文分组，然后计算每个分组的IC指数，如果IC指数接近自然语言，那就说明每组的长度就是密钥长度

原因在于，分组之后，每一列就是一个凯撒密码，因为使用的密钥是一样的

由于凯撒密码只移位，不会改变字母出现的频率，所以IC指数接近自然语言

这个IC指数，就是密文中选出两个相同字母的概率 \[
IC = \frac{\sum_{i=1}^{26} n_i(n_i-1)}{N(N-1)}
\] 如果是随机生成的字母，IC应该是1/26 \[
IC = 26\times \frac{1}{26^2} = \frac{1}{26}\approx 0.038
\] 而自然语言是0.065

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
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
import re
import string
from collections import Counter

ENGLISH_FREQ = [
    0.08167,0.01492,0.02782,0.04253,0.12702,0.02228,
    0.02015,0.06094,0.06966,0.00153,0.00772,0.04025,
    0.02406,0.06749,0.07507,0.01929,0.00095,0.05987,
    0.06327,0.09056,0.02758,0.00978,0.02360,0.00150,
    0.01974,0.00074
]
ALPHABET = string.ascii_lowercase
cip = re.sub('[^a-z]',"",cipher.lower())
def IC(group):
    fre = [0]*26
    for i in range(len(group)):
        fre[ALPHABET.index(group[i])] +=1
    sum = 0
    for i in fre:
        sum += i*(i-1)
    IC = sum / (len(group)*(len(group)-1))
    return IC
ic = []
for keylen in range(1,73):
    if 1:
        groups = [[] for _ in range(keylen)]
        for i in range(len(cip)):
            groups[i%keylen].append(cip[i])
        ic.append((abs(sum([IC(groups[i]) for i in range(len(groups))]) / len(groups)-0.065),keylen,groups))
ic.sort()
def chi(exp,fac):
    chi = 0
    for i,j in zip(exp,fac):
        chi += (i-j)**2 / i
    return chi
def Ceasar(plain,key):
    ciphertext = ''
    for i in range(len(plain)):
        ciphertext += ALPHABET[(ALPHABET.index(plain[i])-key)%26]
    return ciphertext
print("最有可能的密钥长度",ic[0][1])
key = []
for groups in ic[0][2]:
    candidate = []    
    for shift in range(26):
        plain = Ceasar(groups,shift)
        fre = [0 for i in range(26)]
        for j in range(len(plain)): 
            fre[ALPHABET.index(plain[j])] +=1 /len(plain)
        candidate.append(chi(ENGLISH_FREQ,fre))
    key.append(ALPHABET[candidate.index(min(candidate))])  
print("最有可能的密钥","".join(key))
```

求出长度之后，每一列都是一个凯撒加密，直接用词频分析即可

由于前面Kasiski检验最大长度是73，所以我们就检验1到73的IC

输出：

```
1
2
最有可能的密钥长度 48
最有可能的密钥 vigenerevigenerevigenerevigenerevigenerevigenere
```

看着好像不对，怎么会是48呢，但其实这就是6个vigenere合在一起，和一个是没什么区别的，这说明原始文本的长度应该是6的倍数，这样1个和6个其实没差

## 2.流密码
最简单的一次一密

加密 \[
c = m\oplus k
\] 解密 \[
m = c\oplus k
\] 课程中感触比较深的就是可证明安全

比如，证明语义安全，也即密文不会泄露明文信息

假设长度为l，那么

如果在知道密文为c之后，预测明文为m的概率和直接预测是一样的，那就就能证明语义安全
\[
P(M=m) = P(M=m|C=c)
\] 这里可以使用贝叶斯公式 \[
P(M=m|C=c) =
\frac{P(C=c|M=m)P(M=m)}{P(C=c)}=\frac{2^{-l}P(M=m)}{2^{-l}}=P(M=m)
\]

但必须一次一密，如果密钥不换的话，就可以被攻击 \[
c_1 = m_1 \oplus k \\
c_2 = m_2 \oplus k
\]

那么 \[
c_1 \oplus c_2 = m_1 \oplus m_2
\] 这样的两个明文的异或结果会被泄露

## 3.块密码
### 1.Feistel结构
加密过程是 \[
L_{i+1}= R_i \\
R_{i+1}=L_{i}\oplus F(k_{i},R_{i})
\] 解密过程，只需要将输入的R和L换个顺序，然后密钥k反过来

这样的话，加解密是相同的算法，这样就无需设计可逆的F算法

极大的简便了加解密算法

DES加密正是这种结构

### 2.DES加密
先经过一个置换

然后经过Feistel 16轮加密

再逆置换

就得到了密文

解密是非常简单的，由于Feistel结构的优势，这就导致解密速度非常快

### 3.AES加密
比较复杂

首先随机生成一个8字节（128bits）的key，然后我们通过密钥拓展，生成每一轮的key矩阵

然后我们把明文按照每16字节一个块，建立state矩阵

首先根据S盒进行字节替换，subbytes

然后是和state和round_key异或，得到初始状态

然后进行confusion，进行移位和列混淆，也就是shift_row和mixcolumns

(最后一轮不进行列混淆)

## 4.HASH
hash函数就是将\(\{0,1\}^*\)映射到\(\{0,1\}^n\)的函数，即将任意长度的比特串映射为n-bits

即 \[
H = h(M)
\] 其中H叫做像，M是原像

一个好的hash函数需要满足一下属性

#### 1.抗原像攻击
给定H,找到X，使得h(X)=H是困难的

#### 2.抗第二原像攻击（弱抗碰撞）
给定X,找到X'使得h(X)=h(X')是困难的

#### 3.抗碰撞攻击
找到任意两个X和X',满足h(X)=h(X')是困难的

（任何一个第二原像都不存在）

#### hash函数设计
1.先进行填充，使填充后的消息长度为m的整数倍，

2.分组，分为\(M_0,M_1,..M_{t-1}\)

3.压缩，将\(\{0,1\}^{l+m}\)压缩到\(\{0,1\}^{l}\)

令\(H_0=IV(l-bits)\),然后依次计算
\[
H_{i+1}=f(H_i,M_i)
\]

### 1.Merkle–Damgård结构
img将消息分块处理，设置初始iv，然后经过压缩函数处理，最后一轮得到的输出就是hash值

但由于最后附加上了长度，容易受到长度拓展攻击

常见的如MD5，SM3等算法都是采用这种结构

## 5.非对称密码
### RSA
选择两个大素数p，q

将N=pq作为模数

计算欧拉函数 \[
\varphi(n) = (p-1)(q-1)
\] 选择与phi互素的e，计算私钥 \[
de \equiv 1 \mod \varphi(n)
\] 加密 \[
c = m^e \mod n
\] 解密 \[
m = c^d \mod n
\] 有非常多攻击方式，甚至还有侧信道攻击

RSA问题的困难性在于大整数分解的困难性

目前RSA的安全性主要由位数来保证

但同时de泄露也会导致破解，只要知道d，就能分解N \[
de -1 =k\varphi(n)
\] 我们知道kphi，那么可以考虑利用费马小定理得到这个式子

\[
a^{\varphi(n)} \equiv 1 \mod n
\] 那么 \[
a^{k\varphi(n)} \equiv 1 \mod n
\] 对这个式子不断开方

假设 \[
k\varphi(n) = 2^s t
\] 我们随机选择和n互素的a，如果 \[
a^t \not\equiv 1 \mod n
\] 那我们就找到了一个非平凡平方根，那么假设 \[
y_0 = a^t
\] 不断平方，直到 \[
y_j \equiv 1 \mod n,y_{j-1} \not \equiv \pm1 \mod n
\] 一旦找到这样的，那么 \[
n |y_j-1,n|(y_{j-1}-1)(y_{j-1}+1)
\] 那么很明显两个因式都不是n的倍数，那么分别是p，q的倍数

所以 \[
p = gcd(y_{j-1}-1,n)
\]

于是成功因式分解

综述一个课程中讲过的例子

#### 1.A meet-in-the-middle attack
假设明文m是64bits，这个攻击主要针对m是可以分解的，假设m可以分解为
\[
m = m_1m_2
\] 那么一定有一个小于2的32次方

然后注意到 \[
c \equiv m^e \equiv m_1^e m_2^e \mod n
\] 我们假设m1小于2的32次方

那么我们建表 \[
\frac{c}{m_1^e} \mod n
\] 然后再让m2从2的32次方开始遍历，直到找到匹配

这里实现一个36bits的实例

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
from Crypto.Util.number import *
from tqdm import *
m1 = getPrime(18)
m2 = getPrime(18)
m = m1*m2
print(m1,m2,m)
e = 65537
p = getPrime(512)
q = getPrime(512)
n = p*q
c = pow(m,e,n)
table = {}
for m1 in trange(2**18):
    try:
        table[c*inverse(pow(m1,e,n),n)%n] = m1
    except:
        pass
for m2 in trange(2**18):
    if pow(m2,e,n) in table:
        m1 = table[pow(m2,e,n)]
        print("找到了")
        print(m1,m2)
```

## 6.diffie-hellman密钥交换
密码学上的柯克霍夫原则（Kerckhoffs's
principle，也称为柯克霍夫假说、公理、或定律）系由奥古斯特·柯克霍夫在19世纪提出：即使密码系统的任何细节已为人悉知，只要密匙（key，又称密钥或秘钥）未泄漏，它也应是安全的。

因此保证密钥的安全性是非常关键的

Alice和Bob协商选择一个生成元g和模数p

然后Alice选择x作为私钥，Bob选择y作为私钥

Alice和Bob分别计算A和B \[
A= g^x \mod p
\]

\[
B = g^y \mod p
\]

Alice和Bob发送A和B，然后 \[
S = A^y =B^x
\] 双方可以各自计算出密钥S，从而保证了密钥传输的安全

但是容易受到中间人攻击

攻击人只需要在B面前伪装A，在A面前伪装B就行了

## 7.数字签名
主要依靠离散对数的困难性

对称密码由于只有一把密钥，加密和解密都是用同一把密钥，那么很容易受到MIMT攻击，中间人受到一方的信息，就可以用密钥解密，然后随便伪造信息，篡改信息。非对称密码用到了两把密钥，公钥和私钥，一把用于加密，一把用于解密

RSA的方便在于，不需要协商，只要解密方发布一个公钥，任何人都可以用这个公钥来加密

但只有持有私钥的那一方可以解密

那反过来，就可以用作签名

也就是说，签名方用私钥签名，任何人都可以用公钥来验证签名，但只有签名方能生成签名

以ecdsa为例

### 生成签名
协商椭圆曲线 \[
y^2 = x^3+ax+b \mod p
\]

基点G,阶数n，以上这些参数都是公开的

生成私钥\(d_A\),公钥\(Q_A\) \[
d_A \in [1,n-1]
\]

\[
Q_A = d_AG
\]

这个椭圆曲线是选定安全的椭圆曲线，DLP是非常困难的问题，从\(Q_A,G\)几乎不可能恢复出私钥来

计算hash \[
e = Hash(m)
\]

这里要注意，如果e的位数大于n的位数，那么要截断高位 \[
e >> (hlen - nlen)
\]

生成随机数k

计算 \[
kG=(x_1,y_1)
\]

取模得到r \[
r \equiv x_1 \mod n
\]

得到签名 \[
s \equiv k^{-1}(e+rd_A) \mod n
\]

### 验证签名
计算 \[
u_1 = es^{-1} \mod n
\]

\[
u_2 = rs^{-1} \mod n
\]

计算 \[
u_1G+u_2 Q_A = s^{-1}(e+rd_A)G = kG=(x_1,y_1) \mod n
\]

验证 \[
r = x_1 \mod n
\]

容易存在的漏洞就是，随机数k生成不当，可以预测，或是k复用

还有就是曲线参数可以随意替换等等

## 8.消息验证码MAC
消息认证码的输入为任意长度的消息和共享的密钥，它可以输出固定长度的数据，这个数据称为MAC
值。

现在主要使用的是HMAC（基于哈希的消息验证码）

还有cbc-mac等等，cbc-mac的初始向量iv要求全为0

## 9.零知识证明
可以向验证方证明自己知道某个东西，但是又不泄露任何东西

具有三个性质

1. 完备性（Completeness）：若一个证明方确实掌握了某论断的答案，则他肯定能找到方法向验证方证明他手中掌握的数据的正确性，即真的假不了
2. 可靠性（Soundness）：若一证明方根本不掌握某论断的答案，则他无法（或只能以极低概率）说服验证方他手中所谓答案的准确性，即假的真不了。
3. 零知识性(Zero-knowledgeness)：验证方除了知道证明的结果外，对其他信息一无所知。
## 10.TLS协议
TLS是一种用于在网络中加密数据传输的协议，旨在保护数据的机密性、完整性和身份验证。

TLS 是 SSL的继任者，提供了更强的安全性和性能。TLS 是
HTTPS、SMTPS、FTPS 等安全协议的基础。

主要涉及6个步骤

1. ClientHello：客户端发送支持的加密算法列表。
2. ServerHello：服务器选择加密算法并发送服务器证书。
3. 证书验证：客户端验证服务器证书的有效性。
4. 密钥交换：客户端生成预主密钥，用服务器公钥加密后发送。
5. 会话密钥：双方根据预主密钥生成会话密钥，用于加密后续通信。