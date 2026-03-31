---
title: reverse
date: 2025-02-03 12:12:00
categories:
  - 未分类
tags:
  - 导入
---

<!-- 本文是从已发布的 HTML 逆向提取的内容 -->
<!-- 原始文件: 20250203201200.html -->

> ⚠️ 注意: 这是自动从 HTML 提取的内容，可能需要手动调整格式

## 内容预览

密码脚本小子当太多了，脚本写不利索，打打reverse练习一下写脚本的能力 然后reverse里面流密码和块密码挺多的，借此为crypto打下基础 SSH复现 一、Let's go to learn crypto 用idapro打开文件，f5反编译得到 image-20250308161633827 发现里面给了key，但目前还不知道什么加密方法 而后面又有一个base64，就是把明文用base64编码，然后比较base64编码和encflag 那encflag就需要找到Cry_Encrypt函数 image-20250308161803810 打开发现了是AES加密，所以，和逆向没什么关系，直接解密就行了 image-20250308162043119 随便翻一下就找到encflag了，如果翻不到，直接用search搜索也行 1234567from base64 import *from Crypto.Cipher import AESenc_flag = "KKN+NK5ZWN4xr4kM1+qq+2wJKUEEaiWmITgnvi2VaXfjscLoN2sbUObWbnc45pZ

...

*更多内容需要手动补充*

