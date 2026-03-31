---
title: Lilctf2025
date: 2025-08-25 05:37:09
categories:
  - 未分类
tags:
  - 导入
---

<!-- 本文是从已发布的 HTML 逆向提取的内容 -->
<!-- 原始文件: 20250825133709.html -->

> ⚠️ 注意: 这是自动从 HTML 提取的内容，可能需要手动调整格式

## 内容预览

Crypto 1.ez_math 12345678910111213141516171819202122from sage.all import *from Crypto.Util.number import *flag = b'LILCTF{test_flag}'[7:-1]lambda1 = bytes_to_long(flag[:len(flag)//2])lambda2 = bytes_to_long(flag[len(flag)//2:])p = getPrime(512)def mul(vector, c): return [vector[0]*c, vector[1]*c]v1 = [getPrime(128), getPrime(128)]v2 = [getPrime(128), getPrime(128)]A = matrix(GF(p), [v1, v2])B = matrix(GF(p), [mul(v1,lambda1), mul(v2,lambda2)])C = A.inverse() * Bprint(f'p = {p}')print(f'C = {str(

...

*更多内容需要手动补充*

