"""任务一共用的DDT、LAT遍历计算；同一Python进程内，每张表只计算一次。"""

from functools import cache


# CipherFour四位S盒，输入下标依次为0至F。
SBOX = (0x9, 0x8, 0x0, 0x1, 0xE, 0xB, 0xC, 0xD,
        0x3, 0x2, 0x5, 0x7, 0xF, 0xA, 0x6, 0x4)
SIZE = len(SBOX)


@cache
def compute_ddt():
    """返回DDT[a][b]：输入差分a产生输出差分b的输入数量。"""
    table = [[0] * SIZE for _ in range(SIZE)]
    for a in range(SIZE):
        for x in range(SIZE):
            b = SBOX[x] ^ SBOX[x ^ a]
            table[a][b] += 1
    return table


@cache
def compute_lat():
    """返回LAT[a][b]：满足a·x=b·S(x)的输入数量减去8。

    模2内积等于按位与结果中1的个数的奇偶性。
    表项允许为负；后续提取合法掩码对时应使用!=0。
    """
    table = [[0] * SIZE for _ in range(SIZE)]
    for a in range(SIZE):
        for b in range(SIZE):
            equal_count = 0
            for x in range(SIZE):
                input_parity = (a & x).bit_count() & 1
                output_parity = (b & SBOX[x]).bit_count() & 1
                if input_parity == output_parity:
                    equal_count += 1
            table[a][b] = equal_count - SIZE // 2
    return table


def bits(a, b):
    """按(a3,a2,a1,a0,b3,b2,b1,b0)编码，供各建模方法共用。"""
    return [(value >> shift) & 1
            for value in (a, b) for shift in (3, 2, 1, 0)]


def print_table(name, table):
    """只打印表格：输入在行，输出在列，行列下标使用十六进制。"""
    print(f"\n{name}")
    print("     " + " ".join(f"{b:3X}" for b in range(SIZE)))
    for a, row in enumerate(table):
        print(f"{a:2X}:  " + " ".join(f"{value:3d}" for value in row))


if __name__ == "__main__":
    print_table("DDT", compute_ddt())
    print_table("LAT", compute_lat())
