"""
穷举CipherFour算法中满足指定4轮输入、输出差分的所有差分路线

搜索思路:
    (1) 依次枚举全部16比特明文x, 并构造明文对(x, x ^ INPUT_DIFFERENCE).
    (2) 对明文对分别进行4轮CipherFour加密.
    (3) 每轮记录两状态经过S盒和P置换后的差分.
    (4) 只保留最终输出差分等于OUTPUT_DIFFERENCE的明文对.
    (5) 将具有相同4轮差分序列的明文对合并计数.

注: 本程序对全部2^16个x进行计数, 因此每个无序明文对会按两个顺序出现.
路线频率使用count / 2^16计算.
"""

from collections import Counter


# CipherFour算法的S盒定义
S = [9, 8, 0, 1, 14, 11, 12, 13, 3, 2, 5, 7, 15, 10, 6, 4]

# CipherFour算法的P置换定义
P = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]

STATE_SIZE = 2 ** 16
NUMBER_OF_ROUNDS = 4

INPUT_DIFFERENCE = 0x0001
OUTPUT_DIFFERENCE = 0x0010


def S_box(value):
    """对16比特状态的四个半字节分别使用S盒."""
    output = 0

    for shift in [12, 8, 4, 0]:
        output |= S[(value >> shift) & 0xF] << shift

    return output


def P_box(value):
    """对16比特状态进行P置换."""
    input_bits = bin(value)[2:].zfill(16)
    output_bits = ""

    for i in range(16):
        output_bits += input_bits[P[i]]

    return int(output_bits, 2)


def build_SP_table():
    """预先计算全部16比特输入经过一轮S盒和P置换后的结果."""
    SP_table = [0 for _ in range(STATE_SIZE)]

    for value in range(STATE_SIZE):
        SP_table[value] = P_box(S_box(value))

    return SP_table


def find_all_routes(SP_table):
    """搜索并统计满足输入、输出差分条件的所有4轮路线."""
    route_counts = Counter()
    matching_pair_count = 0

    for plainText1 in range(STATE_SIZE):
        plainText2 = plainText1 ^ INPUT_DIFFERENCE
        state1 = plainText1
        state2 = plainText2
        route = []

        for _ in range(NUMBER_OF_ROUNDS):
            state1 = SP_table[state1]
            state2 = SP_table[state2]

            # 只保存每轮经过P置换后的差分状态.
            route.append(state1 ^ state2)

        if route[-1] == OUTPUT_DIFFERENCE:
            route_counts[tuple(route)] += 1
            matching_pair_count += 1

    return route_counts, matching_pair_count


def format_route(route):
    """将差分路线格式化为16进制字符串."""
    differences = (INPUT_DIFFERENCE,) + route
    return " -> ".join("0x%04X" % difference for difference in differences)


if __name__ == "__main__":
    print("输入差分: 0x%04X" % INPUT_DIFFERENCE)
    print("目标输出差分: 0x%04X" % OUTPUT_DIFFERENCE)
    print("正在计算CipherFour的一轮S盒与P置换查找表...")

    SP_table = build_SP_table()
    route_counts, matching_pair_count = find_all_routes(SP_table)

    print("满足输入、输出差分的有序明文对数:", matching_pair_count)
    print(f"不同差分路线数: {len(route_counts)}")
    print(f"目标差分频率: {matching_pair_count / float(STATE_SIZE)}")
    print()
    print("差分路线 | 明文对计数 | 路线频率")
    print("-" * 75)

    total_frequency = 0
    for route, count in sorted(
        route_counts.items(), key=lambda item: (-item[1], item[0])
    ):
        frequency = count / float(STATE_SIZE)
        total_frequency += frequency
        print("%s | %d | %.10f" % (format_route(route), count, frequency))

    print(f"路线总频率为 : {total_frequency}")