'''
第4.1.3节 计算CipherFour算法S盒的线性近似表
这里要修改一下S盒的定义
求解思路:
    (1) 遍历S盒的所有输入掩码alpha.
    (2) 遍历S盒的所有输出掩码beta.
    (3) 对每个输入x, 计算alpha与x的内积.
    (4) 计算beta与Sbox[x]的内积.
    (5) 统计两个内积相等的输入个数, 再减去8.
'''


# CipherFour算法的S盒定义
Sbox = [ 0x9, 0x8, 0x0, 0x1, 0xE, 0xB, 0xC, 0xD, 0x3, 0x2, 0x5, 0x7, 0xF, 0xA, 0x6, 0x4 ]


def get_parity(value):
    """计算一个整数中1的个数的奇偶性."""
    return bin(value).count("1") % 2


def get_linear_table(Sbox):
    """计算4比特S盒的线性近似表LAT."""
    input_all = len(Sbox)
    output_all = len(Sbox)
    linear_table = [
        [0 for beta in range(output_all)]
        for alpha in range(input_all)
    ]

    # 遍历S盒的所有输入掩码alpha
    for alpha in range(input_all):
        # 遍历S盒的所有输出掩码beta
        for beta in range(output_all):
            equal_count = 0

            # 遍历S盒的所有输入x
            for x in range(input_all):
                input_parity = get_parity(x & alpha)
                output_parity = get_parity(Sbox[x] & beta)

                if input_parity == output_parity:
                    equal_count += 1

            linear_table[alpha][beta] = equal_count - input_all // 2

    return linear_table


def print_linear_table(linear_table):
    """按十六进制行列标号打印LAT."""
    print("      ", end="")
    for beta in range(16):
        print("%3X" % beta, end="")
    print()

    for alpha in range(16):
        print("%2X : " % alpha, end="")
        for beta in range(16):
            print("%3d" % linear_table[alpha][beta], end="")
        print()


if __name__ == "__main__":
    linear_table = get_linear_table(Sbox)
    print_linear_table(linear_table)
