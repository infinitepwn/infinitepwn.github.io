---
title: infinite_blog
date: 2025-08-14 16:45:42
tags: []
mathjax: true
---

# Revenge
\[
x_1 \equiv ax_0^2 +bx_0+c \mod m\\
x_2 \equiv ax_1^2 +bx_1+c \mod m\\
x_3 \equiv ax_2^2 +bx_2+c \mod m
\]

第一次差分 \[
x_2-x_1 \equiv a(x_1-x_0)(x_1+x_0)+b(x_1-x_0) \mod m\\
x_3-x_2 \equiv a(x_2-x_1)(x_2+x_1)+b(x_2-x_1) \mod m
\] 记 \[
y_i = x_{i+1}-x_{i}
\]

\[
y_1 \equiv a(x_1-x_0)y_0+by_0 \mod m\\
y_2 \equiv a(x_2-x_1)y_1+by_1 \mod m
\]

第二次差分,消掉b \[
y_1^2-y_2y_0 = ay_0y_1(x_0-x_2)
\] 记 \[
y_i^2-y_{i+1}y_{i-1}=\beta_i\\
y_{i-1}y_{i}(x_{i-1}-x_{i+1})=k_i
\] 那么 \[
\beta_i \equiv k_ia \mod m
\] 于是 \[
\beta_1 \equiv k_1a \mod m \\
\beta_2 \equiv k_2a \mod m\\
\beta_1k_2-\beta_2k_1 \equiv 0 \mod m
\] 所以 \[
\beta_ik_{i+1}-\beta_{i+1}k_i = km
\] 对任意两个\(\beta_ik_{i+1}-\beta_{i+1}k_i\)求gcd+爆破，得到m

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
d = [beta[i]*k[i+1] - beta[i+1]*k[i] for i in range(len(beta)-2)]
m = []
for i in d:
    for j in d:
        if i!=j:
          m.append(gcd(i,j))
m1 = []
for i in m:
    for j in m:
        if i!=j:
          m1.append(gcd(i,j))
km = min(m1)
for i in range(2,2^22):
    if km%i == 0 and km//i < 2**528 and km//i % 65536 == 0:
        m = km//i
```

求出m之后 \[
\beta_1 \equiv k_1a \mod m \\
\] 由于k_1和m有公因数，得除掉 \[
\frac{\beta_1}{(k_1,m)} \equiv \frac{k_1}{(k_1,m)}a \mod
\frac{m}{(k_1,m)}
\] 求出a

```
1
2
3
4
5
d = gcd(k[0],m)
k1 = k[0]//d
b1 = beta[0]//d
m1 = m // d
a = b1*inverse(k1,m1)%m
```

类似的求出b，c

```
1
2
3
d = gcd(y[0],m)
b = (y[1]//d*inverse(y[0]//d,m//d) - a*(x[0]+x[1]))%m
c = (x[1]-a*x[0]^2 - b*x[0])%m
```

然后解二次同余方程 \[
x_0 \equiv a*seed^2+b*seed+c \mod m
\] 由于m不是素数，得crt \[
x_0 \equiv a*seed^2+b*seed+c \mod 65536 \\
x_0 \equiv a*seed^2+b*seed+c \mod \frac{m}{65536}
\] 前者直接枚举爆破65536就行

后者是有限域二次同余方程，都能解

crt合一起，就求出seed