"""统计 PHILOX-2W 一轮在指定输入差分下的输出差分分布。

根据实验指导书中的轮函数文字公式：
    L' = mulhi_M(R)
    R' = mullo_M(R) ^ L ^ K

对每种输入差分穷举全部 2^(2W) 个输入状态，输出出现频率最高的五种差分。
"""

from collections import Counter


W = 8
MODULUS = 1 << W
WORD_MASK = MODULUS - 1
M = 0x9B
ROUND_KEY = 0x46

INPUT_DIFFERENCES = (
    (0x00, 0x01),
    (0x01, 0x00),
    (0x00, 0x02),
    (0x02, 0x01),
)


def mulhi(value):
    """返回 value * M 的高 W 比特。"""
    return (value * M) >> W


def mullo(value):
    """返回 value * M 的低 W 比特。"""
    return (value * M) & WORD_MASK


def philox2w_round(left, right, key=ROUND_KEY):
    """按指导书文字公式执行一轮 PHILOX-2W。"""
    left_out = mulhi(right)
    right_out = mullo(right) ^ left ^ key
    return left_out, right_out


def count_output_differences(input_difference, key=ROUND_KEY):
    """穷举所有输入状态，统计给定输入差分对应的输出差分。"""
    delta_left, delta_right = input_difference
    counts = Counter()

    for left in range(MODULUS):
        for right in range(MODULUS):
            left_prime, right_prime = philox2w_round(left, right, key)
            paired_left_prime, paired_right_prime = philox2w_round(
                left ^ delta_left,
                right ^ delta_right,
                key,
            )

            output_difference = (
                left_prime ^ paired_left_prime,
                right_prime ^ paired_right_prime,
            )
            counts[output_difference] += 1

    return counts


def main():
    state_count = MODULUS**2
    print(f"W: {W}")
    print(f"M: 0x{M:02X}")
    print(f"轮密钥 K: 0x{ROUND_KEY:02X}")
    print(f"每种输入差分遍历的输入状态数: {state_count}")

    for input_difference in INPUT_DIFFERENCES:
        counts = count_output_differences(input_difference)
        top_five = sorted(
            counts.items(),
            key=lambda item: (-item[1], item[0][0], item[0][1]),
        )[:5]

        print()
        print(
            "输入差分 "
            f"({input_difference[0]:02X}, {input_difference[1]:02X})"
        )
        print(f"不同输出差分数: {len(counts)}")
        print("排名 | 输出差分 (ΔL', ΔR') | 计数 | 概率")
        for rank, (output_difference, count) in enumerate(top_five, start=1):
            probability = count / state_count
            print(
                f"{rank:>4} | "
                f"({output_difference[0]:02X}, {output_difference[1]:02X})"
                f"            | {count:>5} | {probability:.10f}"
            )
        print(f"概率总和: {sum(counts.values()) / state_count:.10f}")


if __name__ == "__main__":
    main()
