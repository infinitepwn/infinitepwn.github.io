---
title: XYCTF
date: 2025-04-10 13:50:40
categories:
  - 未分类
tags:
  - 导入
---

<!-- 本文是从已发布的 HTML 逆向提取的内容 -->
<!-- 原始文件: 20250410215040.html -->

> ⚠️ 注意: 这是自动从 HTML 提取的内容，可能需要手动调整格式

## 内容预览

XYCTF wp 1.Division 12345678910111213141516171819202122232425262728293031323334353637import random print('----Welcome to my division calc----')print('''menu: [1] Division calc [2] Get flag''')while True: choose = input(': >>> ') if choose == '1': try: denominator = int(input('input the denominator: >>> ')) except: print('INPUT NUMBERS') continue nominator = random.getrandbits(32) if denominator == '0': print('NO YOU DONT') continue else: print(f'{nominator}//{denominator} = {nominator//denominat

...

*更多内容需要手动补充*

