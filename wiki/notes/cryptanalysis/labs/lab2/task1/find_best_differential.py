"""
搜索CipherFour算法除给定差分外概率最高的4轮差分

搜索思路:
    (1) 计算S盒的差分分布表DDT.
    (2) 对每个非零输入差分, 用动态规划计算4轮后的输出差分概率分布.
    (3) 每轮分别处理4个S盒, 再进行P置换.
    (4) 动态规划会把到达相同差分状态的路线概率相加, 得到差分概率.
    (5) 排除题目给定的差分, 从其余差分中选出概率最高者.

注意: 本程序搜索的是差分概率, 即连接相同输入、输出差分的所有差分路线
概率之和, 不是概率最高的单条差分路线.
"""

import numpy as np
from tqdm import tqdm


# CipherFour算法的S盒定义
S = [9, 8, 0, 1, 14, 11, 12, 13, 3, 2, 5, 7, 15, 10, 6, 4]

# CipherFour算法的P置换定义
P = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]

STATE_SIZE = 2 ** 16
NUMBER_OF_ROUNDS = 4
BATCH_SIZE = 32

# 题目给定的4轮差分, 搜索时排除这一对输入、输出差分
EXCLUDED_INPUT_DIFFERENCE = 0x0001
EXCLUDED_OUTPUT_DIFFERENCE = 0x0001


def diff_T():
    """计算S盒的差分分布表DDT."""
    diff_table = [[0 for _ in range(16)] for _ in range(16)]

    for diff_in in range(16):
        for value in range(16):
            diff_out = S[value] ^ S[value ^ diff_in]
            diff_table[diff_in][diff_out] += 1

    return diff_table


def P_box(value):
    """对16比特差分状态进行P置换."""
    input_bits = bin(value)[2:].zfill(16)
    output_bits = ""

    for i in range(16):
        output_bits += input_bits[P[i]]

    return int(output_bits, 2)


def update_one_sbox_distribution(score, probability_table, position):
    """
    更新一个S盒位置上的差分概率分布.

    score的形状为(batch, 16, 16, 16, 16), 第一维表示不同的输入差分,
    其余四维表示当前16比特差分的四个半字节.
    """
    state_axis = position + 1
    moved_score = np.moveaxis(score, state_axis, -1)
    moved_shape = moved_score.shape

    # 对当前半字节应用DDT. 多条路线到达同一差分时, 概率会在矩阵乘法中相加.
    score_matrix = moved_score.reshape(-1, 16)
    updated_score = score_matrix @ probability_table
    updated_score = updated_score.reshape(moved_shape)

    return np.moveaxis(updated_score, -1, state_axis)


def search_best_differential():
    """搜索排除题目给定差分后的最高概率4轮差分."""
    diff_table = diff_T()
    probability_table = np.array(diff_table, dtype=np.float64) / 16.0

    # 提前计算全部16比特差分经过P置换后的结果.
    permutation = np.array(
        [P_box(value) for value in range(STATE_SIZE)],
        dtype=np.int32,
    )

    best_input_difference = 0
    best_output_difference = 0
    best_probability = 0.0

    total_batches = (STATE_SIZE - 1 + BATCH_SIZE - 1) // BATCH_SIZE

    # 输入差分0对应恒等差分, 不属于本题要搜索的非零差分.
    for batch_index, first_difference in enumerate(
        tqdm(range(1, STATE_SIZE, BATCH_SIZE), desc="批次处理"), start=1
    ):
        input_differences = np.arange(
            first_difference,
            min(first_difference + BATCH_SIZE, STATE_SIZE),
            dtype=np.int32,
        )
        batch_size = len(input_differences)

        # 初始化每个输入差分对应的概率分布, 起始状态的概率为1.
        score = np.zeros((batch_size, 16, 16, 16, 16), dtype=np.float64)
        rows = np.arange(batch_size)
        nibble0 = (input_differences >> 12) & 0xF
        nibble1 = (input_differences >> 8) & 0xF
        nibble2 = (input_differences >> 4) & 0xF
        nibble3 = input_differences & 0xF
        score[rows, nibble0, nibble1, nibble2, nibble3] = 1.0

        # 每轮依次传播四个S盒的差分, 然后进行P置换.
        for _ in range(NUMBER_OF_ROUNDS):
            for position in range(4):
                score = update_one_sbox_distribution(
                    score, probability_table, position
                )

            after_sbox = score.reshape(batch_size, STATE_SIZE)
            after_pbox = np.empty_like(after_sbox)
            after_pbox[:, permutation] = after_sbox
            score = after_pbox.reshape(batch_size, 16, 16, 16, 16)

        # 找出每个输入差分对应概率最高的输出差分.
        output_distribution = score.reshape(batch_size, STATE_SIZE)
        output_differences = np.argmax(output_distribution, axis=1)
        probabilities = output_distribution[rows, output_differences]

        # 排除题目已给出的0001 -> 0001, 但仍允许输入或输出单独为0001.
        excluded_rows = np.flatnonzero(
            input_differences == EXCLUDED_INPUT_DIFFERENCE
        )
        for row in excluded_rows:
            candidate_distribution = output_distribution[row].copy()
            candidate_distribution[EXCLUDED_OUTPUT_DIFFERENCE] = 0.0
            output_differences[row] = np.argmax(candidate_distribution)
            probabilities[row] = candidate_distribution[output_differences[row]]

        row = int(np.argmax(probabilities))
        if probabilities[row] > best_probability:
            best_input_difference = int(input_differences[row])
            best_output_difference = int(output_differences[row])
            best_probability = float(probabilities[row])

        if batch_index % 128 == 0 or batch_index == total_batches:
            print("搜索进度: %d/%d 批" % (batch_index, total_batches))

    return best_input_difference, best_output_difference, best_probability


if __name__ == "__main__":
    print("开始遍历全部非零输入差分, 并累计各差分路线的概率...")
    input_difference, output_difference, probability = search_best_differential()

    print("CipherFour算法除给定差分外概率最高的4轮差分为:")
    print(
        "0x%04X -> 0x%04X"
        % (input_difference, output_difference)
    )
    print("4轮差分概率:", probability)
    print("差分概率的2次幂表示: 2^%.6f" % np.log2(probability))
