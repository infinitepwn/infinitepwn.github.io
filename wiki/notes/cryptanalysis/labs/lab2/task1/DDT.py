'''
例题3.3 计算CipherFour算法S盒的差分分布表

求解思路:
    (1) 遍历S盒的所有输入差分 alpha.
    (2) 对每个输入差分, 遍历S盒的所有输入 x.
    (3) 另一个输入为 x ^ alpha.
    (4) 计算输出差分 beta = Sbox[x] ^ Sbox[x ^ alpha].
    (5) 将差分对 alpha -> beta 在DDT中的计数加1.
'''


# CipherFour算法的S盒定义
Sbox = [9, 8, 0, 1, 14, 11, 12, 13, 3, 2, 5, 7, 15, 10, 6, 4]


def get_diff_table(Sbox):
    """计算4比特S盒的差分分布表DDT."""
    input_all = len(Sbox)
    output_all = len(Sbox)

    # diff_table[alpha][beta]表示输入差分alpha,
    # 输出差分beta出现的次数
    diff_table = [
        [0 for _ in range(output_all)]
        for _ in range(input_all)
    ]

    # 遍历S盒的所有输入差分alpha
    for alpha in range(input_all):
        # 遍历S盒的所有输入x
        for x in range(input_all):
            another_x = x ^ alpha
            beta = Sbox[x] ^ Sbox[another_x]
            diff_table[alpha][beta] += 1

    return diff_table


def print_diff_table(diff_table):
    """按十六进制行列标号打印DDT."""
    print("      ", end="")
    for beta in range(16):
        print("%2X" % beta, end=" ")
    print()

    for alpha in range(16):
        print("%2X : " % alpha, end="")
        for beta in range(16):
            print("%2d" % diff_table[alpha][beta], end=" ")
        print()


if __name__ == "__main__":
    diff_table = get_diff_table(Sbox)
    print_diff_table(diff_table)
