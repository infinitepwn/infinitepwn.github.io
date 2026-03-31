---
title: reverse_note
date: 2025-06-27 14:10:13
tags: ["reverse"]
---

# 1.什么是PE?
PE（ Portable Execute）文件是Windows下可执行文件的总称，常见的有
DLL，EXE，OCX，SYS 等。它是微软在 UNIX 平台的
COFF（通用对象文件格式）基础上制作而成。最初设计用来提高程序在不同操作系统上的移植性，但实际上这种文件格式仅用在
Windows 系列操作系统下。PE文件是指 32
位可执行文件，也称为PE32。64位的可执行文件称为 PE+ 或
PE32+，是PE(PE32)的一种扩展形式（请注意不是PE64)

总而言之就是可执行文件

一个文件是不是可执行文件和后缀名无关

在Linux中，ELF是可执行文件

image-20250627223959874## PE文件的结构包括
DOS头，NT头，节表
以及 具体的节**

### dos头的作用
1. 兼容性：

当PE文件在DOS系统下运行时，DOS头中的代码会执行，通常显示一个错误信息（例如："This program cannot be run in DOS mode."）。
在现代Windows系统中，操作系统会跳过DOS部分，直接解析PE头。

2. 标识PE文件：

DOS头的起始两个字节是魔术字（Magic
Number）MZ（0x4D
0x5A），即MS-DOS的开发者Mark
Zbikowski的缩写。这是判断文件是否为合法PE文件的第一个标志。

image-20250627222244527### DOS头的关键字段
DOS头是一个固定格式的结构（IMAGE_DOS_HEADER），常见重要字段包括：

偏移
字段名
大小（字节）
说明

0x00
e_magic
2
魔术字
MZ（0x4D5A），标识DOS可执行文件。

0x3C
e_lfanew
4
PE头（NT
Headers）的偏移（关键字段！指向PE文件的实际起始位置）。

其他
（如e_cp、e_cblp）
-
DOS遗留字段，现代PE文件中通常无实际用途。

比如这里偏移量是80，也就是128的位置

当一个 PE 文件 被执行时，PE 装载器 首先检查 DOS
header 里的 PE header 的偏移量。如果找到，则直接跳转到 PE header
的位置。

当 PE装载器 跳转到 PE header 后，第二步要做的就是检查 PE header
是否有效。如果该 PE header 有效，就跳转到 PE header 的尾部。

NT头 包含 windows PE 文件的主要信息，其中包括一个
'PE'
字样的签名，PE文件头（IMAGE_FILE_HEADER）和
PE可选头（IMAGE_OPTIONAL_HEADER32）。

### NT头的结构
NT头由三部分组成：

1. PE签名（Signature）
2. 文件头（File Header）
3. 可选头（Optional Header）
其内存布局如下：

```
1
2
3
4
5
IMAGE_NT_HEADERS {
    DWORD Signature;          // PE签名 "PE\0\0" (0x50450000)
    IMAGE_FILE_HEADER FileHeader;
    IMAGE_OPTIONAL_HEADER OptionalHeader;
}
```

紧跟 PE header
尾部的是节表。PE装载器执行完第二步后开始读取节表中的节段信息，并采用文件映射（
在执行一个PE文件的时候，Windows并不在一开始就将整个文件读入内存，而是采用与内存映射的机制，也就是说，Windows装载器在装载的时候仅仅建立好虚拟地址和PE文件之间的映射关系，只有真正执行到某个内存页中的指令或者访问某一页中的数据时，这个页面才会被从磁盘提交到物理内存，这种机制使文件装入的速度和文件大小没有太大的关系
）的方法将这些节段映射到内存，同时附上节表里指定节段的读写属性

# 2.什么是壳？
### 通俗解释：壳（Shell）是什么？
在逆向工程中，“壳”
就像给程序穿了一件“隐身衣”或“防弹衣”，主要做两件事： 1.
隐藏程序（不让别人轻易看到代码逻辑）。 2.
保护程序（防止被破解、篡改或分析）。

### 举个栗子 🌰
假设你写了一个程序，就像一封信： -
没加壳：别人直接打开信就能看到全部内容（代码逻辑、关键数据）。
-
加了壳：信被锁进一个保险箱（壳），只有知道密码（解密逻辑）才能看到原始内容。

### 壳的两种主要类型
1. 压缩壳（如UPX）

作用：把程序“压缩”变小，运行时会自动解压。

例子：就像用zip压缩文件，运行时再解压。

目的：减小文件体积，但容易被脱壳（逆向还原）。

2. 加密壳/保护壳（如VMProtect、Themida）

作用：用加密、混淆、虚拟机等技术保护代码。

例子：像把信写成密文，还混入一堆乱码，只有特定方式能解密。

目的：防止破解（常用于游戏、商业软件、恶意软件）。

### 壳在逆向中的影响
- 增加分析难度：
直接打开加壳的程序，看到的是一堆无意义的代码（壳的代码），真正的逻辑被藏起来了。
- 需要“脱壳”：
逆向工程师要用工具（如OllyDbg、x64dbg）或手动调试，找到“脱壳点”还原原始程序。
### 现实类比
- 压缩壳 ≈ 快递打包（拆开就能拿到东西）。

- 加密壳 ≈
保险箱+密码+自毁装置（需要专业技巧打开）。
恶意软件常用强壳（如VMProtect）躲避杀毒软件分析，而普通软件可能只用压缩壳（如UPX）减小体积。

### 一句话总结
壳就是程序的“外包装”，要么为了压缩，要么为了防破解，让逆向工程师头疼的东西！
想分析它？先脱壳！（就像拆快递一样，有的容易撕开，有的得用电锯🔥）

### 使用exeinfo判断是否有壳
无壳

image-20250627223221855up壳

image-20250628145151630可以用upx脱壳

image-20250628150540713## 3.动态调试
对于一些魔改算法，可以直接动态调试，按F9步进

比如LitCTF2025的

## 4.NSS
### 1.ezC
```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
#include <stdio.h>
#include <string.h>

int main(){
    char a[]="wwwwwww";
    char b[]="d`vxbQd";
//try to find out the flag
printf("please input flag:");
scanf(" %s",&a);

if(strlen(a)!=7){
    printf("NoNoNo\n");
    system("pause");
    return 0;
}

for(int i=0;i<7;i++){
    a[i]++;
    a[i]=a[i]^2;
}

if(!strcmp(a,b)){
    printf("good!\n");
    system("pause");
    return 0;
}

printf("NoNoNo\n");
system("pause");
return 0;
//flag 记得包上 NSSCTF{} 再提交!!!
}
```

直接逆向即可，先异或2再减1

image-20250628143113629### 2.ez_re
有UPX壳，先脱掉

经过反编译，得到

逻辑就是a,通过func，可以得到encode_a

然后最后要求让encode_s = a,相当问，什么东西通过func,可以得到a

首先a是

SERDVEZ7WTB1X2hAdjJfL1wvXEA1N2VyM2RfN2hlX3IzdjNyczN9

encode_a是

U0VSRFZFWjdXVEIxWDJoQWRqSmZMMXd2WEVBMU4yVnlNMlJmTj

一般这种情况我们猜测f3是可逆的，我们把encode_a输入进去

结果得到

VTBWU1JGWkZXamRYVkVJeFdESm9RV1JxU21aTU1YZDJXRVZCTV

明显字符串长度都变了，那该怎么办呢？

正在冥思苦想之际，结果看了wp发现，这就是个base64.。。

image-20250704113040011### 3.Feature
在IDA
Pro（交互式反汇编器）中，"unk"是"unknown"（未知）的缩写，表示IDA无法自动识别该地址处的数据类型或内容。让我详细解释"unk"的含义、原因和处理方法：

1. "unk"的基本含义
- unk_XXXXXX（如unk_480080）表示地址XXXXXX处的数据尚未被IDA识别
- 常见形式：

unk_480080：未知数据块
byte_480080：未知字节数据
word_480080：未知字（2字节）数据
dword_480080：未知双字（4字节）数据
qword_480080：未知四字（8字节）数据

1. 为什么会出现"unk"？

原因
说明
示例

未分析的数据
IDA未识别为代码或已知数据类型
程序中的加密数据、资源文件

混合数据区
代码与数据混合的区域
跳转表、内联数据

动态生成数据
运行时计算的数据地址
加壳程序的解密代码

编译器优化
非常规数据布局
结构体填充字节

反汇编限制
分析深度不足
复杂控制流后的数据

1. 在您代码中的具体例子
c

```
1
2
3
v7 = &unk_480080;  // 指向未知数据区
v8 = 53i64;        // 数据长度53字节
sub_460310(v15, &v7, &v16);  // 使用这个数据
```

- unk_480080 很可能是：

加密密钥
预定义的验证数据
资源字符串
常量数组

总而言之，unk很有可能就是密文，密钥相关的东西

核心逻辑就是

```
1
2
if ( v11 == v15 )
  printf("Congratulations!");
```

所以就需要探源，v11,v15来源

v15只在一处出现过

```
1
sub_460310(v15, &v7, &v16);
```

那么就继续看这个函数

```
1
2
3
4
5
6
7
8
9
10
11
sub_460310(__int64 a1, __int64 a2, __int64 a3)
{
  unsigned int v3; // edi
  __int64 v5; // rsi
  __int64 v6; // rax

  sub_44AC10(a1, a3);
  v5 = sub_4241E0(a2);
  v6 = sub_424240(a2);
  return sub_4601A0(a1, v6, v5, v3);
}
```

考察一下，v7和，v16

```
1
2
3
4
sub_43EE50(&v16);
 v7 = &unk_480080;
 v8 = 53i64;
 sub_460310(v15, &v7, &v16);
```

这个v8就是说,v7的长度是53，v16是一个常量

```
1
2
3
4
5
6
while ( (unsigned __int8)neq(v10, &v9) )
  {
    v18 = *(_DWORD *)eq(v10);
    sub_468200(&qword_47F740, (unsigned int)(char)v18);
    sub_41F310(v10);
  }
```

这是一个输出，那么也就可以推断

v14=LitCTF2025不过没什么用

唯一使用过v11的函数是

```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
sub_4014F0((__int64)v11, v12, v14);
sub_4014F0(__int64 a1, _QWORD *a2, _QWORD *a3)
{
    sub_43EE50((__int64)&v9);
    v10 = 0;
    sub_4603B0(v8, v11, &v10, &v9);
    sub_43EEC0(&v9);
    for ( i = 0; i < strlen(a2); ++i )
    {
      for ( j = 0; j < strlen(a3); ++j )
      {
        v4 = a2[i];
        v5 = a3[j]* v4;
        v6 = v8[i+j];
        *v6 += v5;
      }
    }
    a1=v8;
  return a1;
}
```

大概是这么个意思，也就是v12和v14一起生成了v11

而我们发现v14长度是10

```
1
2
3
v7 = &unk_480160;
v8 = 10i64;
sub_460310(v14, &v7, &v17);
```

所以这里的v7其实就是v14，那么可以猜测v7就是密钥,那么v15反正就是密文

然后根据题目提示，这是一个卷积

就是说，已知卷积，求原来的向量

卷积公式

假设f有m元素 \[
(f*g)[n] = \sum_{i=0}^{m-1}f[i]g[n-i]
\]
注意ida中如果用整型存储字符串，是小端序存储的，所以要倒过来（字符串就不用）