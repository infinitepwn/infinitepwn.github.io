---
title: sympy库的使用
date: 2025-07-10 09:28:22
categories:
  - 未分类
tags:
  - 导入
---

<!-- 本文是从已发布的 HTML 逆向提取的内容 -->
<!-- 原始文件: 20250710172822.html -->

> ⚠️ 注意: 这是自动从 HTML 提取的内容，可能需要手动调整格式

## 内容预览

✅ 1. 创建矩阵 1234from sympy import Matrix, symbolsA = Matrix([[1, 2], [3, 4]])print(A) 输出： 123Matrix([[1, 2],[3, 4]]) 也可以使用符号变量： 12x, y = symbols('x y')B = Matrix([[x, 1], [2, y]]) ✅ 2. 矩阵基本属性 1234print(A.shape) # (2, 2)print(A.rows) # 2print(A.cols) # 2print(A[0, 1]) # 2：访问元素（行列从0开始） ✅ 3. 矩阵加法、乘法、数乘 1234B = Matrix([[5, 6], [7, 8]])print(A + B) # 加法print(A * B) # 矩阵乘法print(2 * A) # 数乘 ✅ 4. 行列式与逆矩阵 12print(A.det()) # 行列式：-2print(A.inv()) # 逆矩阵 注意：只有在行列式不为 0 的情况下才有逆。 ✅ 5. 求解线性方程组 \(Ax = b\) 例：解 \(\be

...

*更多内容需要手动补充*

