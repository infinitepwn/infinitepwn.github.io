"""统计 16 位随机置换在指定输入差分下的输出差分分布。"""

import random

W = 8
MODULUS = 1 << W
INPUT_DIFFERENCES = (
    (0x00, 0x01),
    (0x01, 0x00),
    (0x00, 0x02),
    (0x02, 0x01),
)

STATE_SIZE = 1 << (2 * W)
RANDOM_SEED = 20261009
TOP_COUNT = 5


def pack_words(left, right):
    """将两个 W 比特分支编码成一个 2W 比特状态。"""
    return (left << W) | right


def unpack_words(state):
    """将一个 2W 比特状态拆分为两个 W 比特分支。"""
    return (state >> W) & (MODULUS - 1), state & (MODULUS - 1)


def build_random_permutation(seed=RANDOM_SEED):
    """使用固定种子生成 0 到 2^(2W)-1 的均匀随机排列。"""
    permutation = list(range(STATE_SIZE))
    random.Random(seed).shuffle(permutation)
    return permutation


def count_permutation_output_differences(permutation, input_difference):
    """统计随机置换对给定输入差分产生的输出差分。"""
    delta_state = pack_words(*input_difference)
    counts = {}

    for state in range(STATE_SIZE):
        paired_state = state ^ delta_state
        output_difference = permutation[state] ^ permutation[paired_state]
        output_words = unpack_words(output_difference)
        counts[output_words] = counts.get(output_words, 0) + 1

    return counts


def top_differences(counts, limit=TOP_COUNT):
    """按计数降序、差分数值升序返回排名靠前的输出差分。"""
    return sorted(
        counts.items(),
        key=lambda item: (-item[1], item[0][0], item[0][1]),
    )[:limit]


def print_top_differences(title, counts):
    """打印某种映射的前五个输出差分及其经验概率。"""
    print(title)
    print("排名 | 输出差分 (ΔL', ΔR') | 计数 | 概率")

    for rank, (difference, count) in enumerate(
        top_differences(counts), start=1
    ):
        print(
            f"{rank:>4} | ({difference[0]:02X}, {difference[1]:02X})"
            f"            | {count:>5} | {count / STATE_SIZE:.10f}"
        )

    print(f"观察到的不同输出差分数: {len(counts)}")
    print(f"频率总和: {sum(counts.values()) / STATE_SIZE:.10f}")


def main():
    permutation = build_random_permutation()
    expected_random_probability = 1 / (STATE_SIZE - 1)

    print("随机置换差分统计")
    print(f"分支宽度 W: {W} bit")
    print(f"随机置换种子: {RANDOM_SEED}")
    print(f"状态空间大小: {STATE_SIZE}")
    print(
        "随机置换对任一非零输出差分的理论平均概率: "
        f"{expected_random_probability:.10f}"
    )

    for input_difference in INPUT_DIFFERENCES:
        label = (
            f"输入差分 ({input_difference[0]:02X}, "
            f"{input_difference[1]:02X})"
        )
        print(f"\n{label}")

        random_counts = count_permutation_output_differences(
            permutation,
            input_difference,
        )

        print_top_differences("随机置换输出差分:", random_counts)


if __name__ == "__main__":
    main()
