---
title: reverse常见函数
date: 2025-07-04 14:10:13
categories:
  - 未分类
tags:
  - 导入
---

<!-- 本文是从已发布的 HTML 逆向提取的内容 -->
<!-- 原始文件: 20250704221013.html -->

> ⚠️ 注意: 这是自动从 HTML 提取的内容，可能需要手动调整格式

## 内容预览

逆向积累 1.字符串相等 这里i64相当于LL 0i64=0LL,1i64=1LL 12345678910111213141516__int64 __fastcall equal(_QWORD *a1, _QWORD *a2){ __int64 v2; // rbx int v4; // ebx unsigned __int64 i; // [rsp+28h] [rbp-58h] v2 = sub_425120(a1); if ( v2 != sub_425120(a2) ) return 0i64; for ( i = 0i64; sub_425120(a1) > i; ++i ) { v4 = *(_DWORD *)sub_425200(a1, i); if ( v4 != *(_DWORD *)sub_425200(a2, i) ) return 0i64; } return 1i64; 1234__int64 __fastcall sub_425120(_QWORD *a1){ return (__int64)(a1[1] - *a1) >> 2;} 这个函数获取了a1这个数组

...

*更多内容需要手动补充*

