---
title: recurision
date: 2024-11-12 05:25:12
tags: ["C++"]
mathjax: true
---

### 函数递归
即函数内部调用自身，然后不停地寻找可以返回的值

因此递归必须要设置终止调用链

如使用if语句，在初始值处停止调用，return 初始值

下面是斐波那契数列的一个例子

```
int fibonacciRecurs(int a1,int a2,int n)
{
    if(n == 1 || n == 2)
    {
        return a1;
    }
    int an = fibonacciRecurs(a1,a2,n-1) +fibonacciRecurs(a1,a2,n-2);
    return an;
}

```

由于递归过程中每次函数内部的变量都会被重新初始化，因此可以考虑多传入参数

下面是求反转数字的例子

```
int sum = 0;
int reverseNumber(int n,int sum)
{
	if(n>= 10)
	{
		sum = sum * 10 + n % 10;
		return reverseNumber(n/10,sum)
	}
	sum = sum * 10 + n % 10;
	return sum；
}
```

其中不断地调用自身，可以实现类似循环的功能，

递归的次数就是循环的次数

我们可以使用python简单比较一下循环和递归

```
def peach(n):
	peach = 1
	for i in range(10-n):
		peach = peach * 2 +1 //这是一个计算n天后桃子总数的函数
	return peach
for j in range(10,0,-1):
	print(peach(j))
```

如果使用递归

```
def peach(n):
    if n == 1:
        return 1
    else:
        return  peach(n-1) * 2 + 1
print(peach(5))
```

递归的思路就是把一个复杂的问题，变为简单的问题

但要设置结束条件