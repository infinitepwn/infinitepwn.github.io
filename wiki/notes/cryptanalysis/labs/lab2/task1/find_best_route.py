"""
练习3.2 CipherFour算法的4轮最优差分路线的搜索程序

搜索思路:
    (1) 首先计算S盒的差分分布表DDT.
    (2) 对所有2^16-1个非零输入差分同时进行搜索.
    (3) 每一轮依次计算4个S盒的最大传播概率, 再进行P置换.
    (4) 保存每轮到达各个差分状态的最大概率, 最后倒推出完整路线.

注意: 本程序搜索的是概率最高的单条差分路线(differential trail), 不是将相同输入, 输出差分之间的多条路线概率相加.
"""

import numpy as np


# CipherFour算法的S盒定义
S = [9, 8, 0, 1, 14, 11, 12, 13, 3, 2, 5, 7, 15, 10, 6, 4]

# CipherFour算法的P置换定义
P = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]


def diff_T():
    """计算S盒的差分分布表DDT."""
    diff_table = [[0 for _ in range(16)] for _ in range(16)]

    # 遍历所有输入差分
    for diff_in in range(16):
        # 遍历S盒的所有输入
        for x1 in range(16):
            x2 = x1 ^ diff_in
            diff_out = S[x1] ^ S[x2]
            diff_table[diff_in][diff_out] += 1

    return diff_table


def P_box(value):
    """对16比特差分状态进行P置换."""
    bin_value = bin(value)[2:].zfill(16)
    output = ""

    for i in range(16):
        output += bin_value[P[i]]

    return int(output, 2)


def split_nibbles(value):
    """将16比特状态拆成4个4比特差分."""
    return [
        (value >> 12) & 0xF,
        (value >> 8) & 0xF,
        (value >> 4) & 0xF,
        value & 0xF,
    ]


def update_one_sbox(score, probability_table, position):
    """
    对指定位置的一个S盒进行差分传播.

    score是一个16*16*16*16的数组, 四个下标分别表示
    一个16比特差分的四个半字节.
    """
    new_score = np.zeros_like(score)

    for diff_in in range(16):
        for diff_out in range(16):
            probability = probability_table[diff_in][diff_out]

            # DDT中计数为0, 说明该传播不可能
            if probability == 0:
                continue

            # 对当前半字节取最大路线概率
            if position == 0:
                candidate = score[diff_in, :, :, :] * probability
                new_score[diff_out, :, :, :] = np.maximum(
                    new_score[diff_out, :, :, :], candidate
                )
            elif position == 1:
                candidate = score[:, diff_in, :, :] * probability
                new_score[:, diff_out, :, :] = np.maximum(
                    new_score[:, diff_out, :, :], candidate
                )
            elif position == 2:
                candidate = score[:, :, diff_in, :] * probability
                new_score[:, :, diff_out, :] = np.maximum(
                    new_score[:, :, diff_out, :], candidate
                )
            else:
                candidate = score[:, :, :, diff_in] * probability
                new_score[:, :, :, diff_out] = np.maximum(
                    new_score[:, :, :, diff_out], candidate
                )

    return new_score


def search_best_route():
    """搜索4轮CipherFour的全局最优单条差分路线."""
    diff_table = diff_T()

    # 将DDT计数转换为S盒差分传播概率
    probability_table = []
    for diff_in in range(16):
        row = []
        for diff_out in range(16):
            row.append(diff_table[diff_in][diff_out] / 16.0)
        probability_table.append(row)

    # 提前计算全部16比特状态的P置换结果
    permutation = np.array([P_box(x) for x in range(2 ** 16)])

    # best_probability[r][d]表示经r轮后到达差分d的最大单条路线概率
    best_probability = []

    # 允许所有非零输入差分, 初始概率设为1
    first_round_input = np.ones(2 ** 16)
    first_round_input[0] = 0.0
    best_probability.append(first_round_input)

    # 向前计算4轮的最大概率
    for round_index in range(4):
        score = best_probability[round_index].reshape(16, 16, 16, 16)

        # 依次处理4个并行S盒
        for position in range(4):
            score = update_one_sbox(score, probability_table, position)

        after_sbox = score.reshape(2 ** 16)

        # 将S盒输出差分经过P置换
        after_pbox = np.zeros(2 ** 16)
        after_pbox[permutation] = after_sbox
        best_probability.append(after_pbox)

    # 找到4轮后概率最大的输出差分
    current_difference = int(np.argmax(best_probability[4]))
    route = [current_difference]
    round_probabilities = []

    # 从第4轮向第1轮倒推最优路线
    for round_index in range(4, 0, -1):
        # P是对合置换, 所以再过一次P即可得到S盒输出
        sbox_output = P_box(current_difference)
        output_nibbles = split_nibbles(sbox_output)

        best_predecessor = 0
        best_value = -1.0
        best_one_round_probability = 0.0

        # 遍历上一轮的全部差分状态
        for predecessor in range(2 ** 16):
            predecessor_probability = best_probability[round_index - 1][predecessor]
            if predecessor_probability == 0:
                continue

            input_nibbles = split_nibbles(predecessor)
            one_round_probability = 1.0

            for position in range(4):
                one_round_probability *= probability_table[
                    input_nibbles[position]
                ][output_nibbles[position]]

            candidate = predecessor_probability * one_round_probability

            if candidate > best_value:
                best_value = candidate
                best_predecessor = predecessor
                best_one_round_probability = one_round_probability

        route.append(best_predecessor)
        round_probabilities.append(best_one_round_probability)
        current_difference = best_predecessor

    route.reverse()
    round_probabilities.reverse()

    total_probability = 1.0
    for probability in round_probabilities:
        total_probability *= probability

    return route, round_probabilities, total_probability


if __name__ == "__main__":
    route, round_probabilities, total_probability = search_best_route()

    print("CipherFour算法的4轮最优差分路线为:")
    print(" -> ".join(hex(x)[2:].zfill(4).upper() for x in route))
    print("各轮概率为:", round_probabilities)
    print("总概率:", total_probability, "= 2^" + str(int(np.log2(total_probability))))