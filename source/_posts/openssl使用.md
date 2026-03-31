---
title: openssl使用
date: 2025-07-11 11:45:17
categories:
  - 未分类
tags:
  - 导入
---

<!-- 本文是从已发布的 HTML 逆向提取的内容 -->
<!-- 原始文件: 20250711194517.html -->

> ⚠️ 注意: 这是自动从 HTML 提取的内容，可能需要手动调整格式

## 内容预览

BIGNUM（大数） BIGNUM 是 OpenSSL 里用于存储大整数的结构体，远超普通的 int 或 long，适合密码学中用到的大数运算。 常用操作函数示例： BN_new() — 创建一个新的大数对象。 BN_free() — 释放大数对象。 BN_hex2bn(BIGNUM **bn, const char *hex) — 从十六进制字符串创建大数。 BN_bn2hex(const BIGNUM *bn) — 把大数转成十六进制字符串。 BN_mod_inverse() — 计算模逆。 BN_mod_mul() — 模乘。 BN_mod_add() — 模加。 BN_rand_range() — 生成范围内随机数。 BN_CTX 是大数计算时的临时变量池，避免频繁申请释放内存。 使用流程： BN_CTX_new() 创建。 BN_CTX_start() 开始申请临时变量。 BN_CTX_get() 依次申请临时变量（BIGNUM指针）。 计算结束后用 BN_CTX_end() 和 BN_CTX_free() 清理。 EC_GROUP 代表一个椭圆曲线参数集合，例如素域p，系数

...

*更多内容需要手动补充*

