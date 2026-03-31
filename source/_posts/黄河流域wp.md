---
title: 黄河流域wp
date: 2025-05-25 09:54:00
categories:
  - 未分类
tags:
  - 导入
---

<!-- 本文是从已发布的 HTML 逆向提取的内容 -->
<!-- 原始文件: 20250525175400.html -->

> ⚠️ 注意: 这是自动从 HTML 提取的内容，可能需要手动调整格式

## 内容预览

黄河流域WP1.LatticeLWE问题 123456789101112131415161718192021222324252627282930def gen(q, n, N, sigma): t = np.random.randint(0, high=q // 2, size=n) s = np.concatenate([np.ones(1, dtype=np.int32), t]) A = np.random.randint(0, high=q // 2, size=(N, n)) e = np.round(np.random.randn(N) * sigma**2).astype(np.int32) % q b = ((np.dot(A, t) + e).reshape(-1, 1)) % q P = np.hstack([b, -A]) return P, sdef enc(P, M, q): N = P.shape[0] n = len(M) r = np.random.randint(0, 2, (n, N)) Z = np.zeros((n, P.shape[1]), d

...

*更多内容需要手动补充*

