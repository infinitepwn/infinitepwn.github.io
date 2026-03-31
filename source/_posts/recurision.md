---
title: recurision
date: 2024-11-12 05:25:12
categories:
  - 未分类
tags:
  - 导入
---

<!-- 本文是从已发布的 HTML 逆向提取的内容 -->
<!-- 原始文件: 20241112132512.html -->

> ⚠️ 注意: 这是自动从 HTML 提取的内容，可能需要手动调整格式

## 内容预览

函数递归即函数内部调用自身，然后不停地寻找可以返回的值 因此递归必须要设置终止调用链 如使用if语句，在初始值处停止调用，return 初始值 下面是斐波那契数列的一个例子 12345678910int fibonacciRecurs(int a1,int a2,int n){ if(n == 1 || n == 2) { return a1; } int an = fibonacciRecurs(a1,a2,n-1) +fibonacciRecurs(a1,a2,n-2); return an;} 由于递归过程中每次函数内部的变量都会被重新初始化，因此可以考虑多传入参数 下面是求反转数字的例子 1234567891011int sum = 0;int reverseNumber(int n,int sum){ if(n>= 10) { sum = sum * 10 + n % 10; return reverseNumber(n/10,sum) } sum = sum * 10 + n % 10; return sum；} 其中不断地调用自身，可以实现类似循环的功能， 递归的次数就是

...

*更多内容需要手动补充*

