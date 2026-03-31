---
title: RSA相关总结
date: 2025-07-29 06:08:15
categories:
  - 未分类
tags:
  - 导入
---

<!-- 本文是从已发布的 HTML 逆向提取的内容 -->
<!-- 原始文件: 20250729140815.html -->

> ⚠️ 注意: 这是自动从 HTML 提取的内容，可能需要手动调整格式

## 内容预览

RSA简介 1.encrypt 生成两个大素数p,q 计算 作为模数，计算Euler函数 然后随机生成公钥e,满足 当N，e公开作为公钥之后 任何人都可以用公钥加密 2.decrypt 计算私钥 解密 只有拥有私钥d的人可以解密 但是，往往由于参数生成不当，RSA可以被破解 相关数论算法 1.Eculid算法 用一个递归很容易实现 123456def eculid(x,y): r = x % y if r == 0: return y else: return eculid(y,r) 时间复杂度是O() 2.Extend Eculid算法 也是递归 123456def gcdext(x,y): r = x % y if r == 0: return [0,1] else: return [gcdext(y,r)[1],gcdext(y,r)[0] - x//y * gcdext(y,r)[1]] 注意到 由于x可以由y和x%y表示，那么 只需求 的解，注意到 那么 即 此算法可以直接由gmpy2的库调用，即gmpy2.gcdext 返回的是d,x,y的元组 公钥e相关攻击 1.smal

...

*更多内容需要手动补充*

