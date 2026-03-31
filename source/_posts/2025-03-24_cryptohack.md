---
title: cryptohack
date: 2025-03-24 12:40:00
tags: ["CTF crypto"]
---

### 1.marin
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
#!/usr/bin/env python3

import random
from Crypto.Util.number import bytes_to_long
from secret import secrets, flag

def get_prime(secret):
    prime = 1
    for _ in range(secret):
        prime = prime << 1
    return prime - 1

random.shuffle(secrets)

m = bytes_to_long(flag)
p = get_prime(secrets[0])
q = get_prime(secrets[1])
n = p * q
e = 0x10001
c = pow(m, e, n)

print(f"n = {n}")
print(f"e = {e}")
print(f"c = {c}")

```

注意到  假设b大于a，然后我们只需要不断除以2，就可以知道a等于多少