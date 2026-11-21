"""
随机选取5组密钥, 测试4轮CipherFour的差分出现频率

实验思路:
    (1) 随机生成5组互不相同的轮密钥, 每组包含5个16比特密钥字.
    (2) 对每组密钥, 计算全部16比特明文的4轮CipherFour密文.
    (3) 枚举输入差分为INPUT_DIFFERENCE的明文对.
    (4) 统计输出差分等于OUTPUT_DIFFERENCE的明文对数及其频率.
    (5) 计算5组密钥下输出差分频率的平均值.

注: 每组加密包含4轮S盒和P置换, 最后一轮也包含P置换;
    第5个密钥字在全部轮函数之后与状态异或.
"""

import random


# CipherFour算法的S盒定义
S = [9, 8, 0, 1, 14, 11, 12, 13, 3, 2, 5, 7, 15, 10, 6, 4]

# CipherFour算法的P置换定义
P = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]

STATE_SIZE = 2 ** 16
NUMBER_OF_ROUNDS = 4
TRIALS = 5
SEED = 20261001

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


def cipherFourEnc(plainText, keys, SP_table):
    """使用5个轮密钥字执行4轮CipherFour加密, 每轮均包含P置换."""
    state = plainText

    for round_index in range(NUMBER_OF_ROUNDS):
        state = SP_table[state ^ keys[round_index]]

    return state ^ keys[NUMBER_OF_ROUNDS]


def generate_key_sets(trials=TRIALS, seed=SEED):
    """生成指定数量且互不相同的5字密钥组."""
    rng = random.Random(seed)
    key_sets = []
    used_key_sets = set()

    while len(key_sets) < trials:
        keys = tuple(rng.randrange(STATE_SIZE) for _ in range(NUMBER_OF_ROUNDS + 1))

        if keys not in used_key_sets:
            used_key_sets.add(keys)
            key_sets.append(keys)

    return key_sets


def run_experiment(trials=TRIALS, seed=SEED):
    """统计每组密钥下指定输出差分的出现次数和频率."""
    SP_table = build_SP_table()
    key_sets = generate_key_sets(trials, seed)
    results = []

    for keys in key_sets:
        cipherText = [
            cipherFourEnc(plainText, keys, SP_table)
            for plainText in range(STATE_SIZE)
        ]

        count = 0
        for plainText in range(STATE_SIZE):
            paired_plainText = plainText ^ INPUT_DIFFERENCE
            if (
                cipherText[plainText] ^ cipherText[paired_plainText]
                == OUTPUT_DIFFERENCE
            ):
                count += 1

        frequency = count / float(STATE_SIZE)
        results.append((keys, count, frequency))

    return results


if __name__ == "__main__":
    print(f"输入差分: {hex(INPUT_DIFFERENCE)}")
    print(f"目标输出差分: {hex(OUTPUT_DIFFERENCE)}")
    print(f"密钥组数:{TRIALS}")
    print(f"随机种子: {SEED}")
    print()
    print("序号 | 轮密钥组 | 匹配对数 | 输出差分频率")
    print("-" * 88)

    results = run_experiment()

    for index, (keys, count, frequency) in enumerate(results, start=1):
        key_text = "[" + ", ".join("0x%04X" % key for key in keys) + "]"
        print(
            "%4d | %s | %8d | %.10f"
            % (index, key_text, count, frequency)
        )

    average_frequency = sum(result[2] for result in results) / len(results)
    print("-" * 88)
    print("平均输出差分频率: %.10f" % average_frequency)
