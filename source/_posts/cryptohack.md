---
title: cryptohack
date: 2025-03-24 12:40:00
categories:
  - 未分类
tags:
  - 导入
---

<!-- 本文是从已发布的 HTML 逆向提取的内容 -->
<!-- 原始文件: 20250324204000.html -->

> ⚠️ 注意: 这是自动从 HTML 提取的内容，可能需要手动调整格式

## 内容预览

1.marin 123456789101112131415161718192021222324252627#!/usr/bin/env python3import randomfrom Crypto.Util.number import bytes_to_longfrom secret import secrets, flagdef get_prime(secret): prime = 1 for _ in range(secret): prime = prime << 1 return prime - 1random.shuffle(secrets)m = bytes_to_long(flag)p = get_prime(secrets[0])q = get_prime(secrets[1])n = p * qe = 0x10001c = pow(m, e, n)print(f"n = {n}")print(f"e = {e}")print(f"c = {c}") 注意到 假设b大于a，然后我们只需要不断除以2，就可以知道a等于多少

...

*更多内容需要手动补充*

