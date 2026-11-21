"""
任务4：对5轮CipherFour明密文对进行去噪，并恢复K6的一个半字节.

加密结构:
    第1至第4轮: 异或轮密钥、过S盒、拉线置换.
    第5轮: 异或轮密钥K5、过S盒，不做拉线置换.
    最后: 异或白化密钥K6.

四轮目标差分为0x0010. 第五轮S盒后，正确对的密文差分只能是
0x0010、0x0020或0x0050. 程序根据密文差分筛选，再对K6中对应半字节
的16种候选进行部分解密计数.

明密文数据读取自labs/lab2/code/plaintext.txt和ciphertext.txt.
"""

from pathlib import Path


# CipherFour算法的S盒及其逆S盒.
S = [9, 8, 0, 1, 14, 11, 12, 13, 3, 2, 5, 7, 15, 10, 6, 4]
S_REVERSE = [2, 3, 9, 8, 15, 10, 14, 11, 1, 0, 13, 5, 6, 7, 4, 12]

INPUT_DIFFERENCE = 0x0001
FOUR_ROUND_DIFFERENCE = 0x0010
ACTIVE_NIBBLE_SHIFT = 4
ACTIVE_NIBBLE_DIFFERENCE = (FOUR_ROUND_DIFFERENCE >> ACTIVE_NIBBLE_SHIFT) & 0xF
ALLOWED_SBOX_OUTPUT_DIFFERENCES = {0x1, 0x2, 0x5}
STATE_SIZE = 1 << 16

# 参考数据使用的六个密钥字K1,...,K6.
# 已知密钥仅用于程序结束时核对猜测结果，不参与筛选和候选计数.
ROUND_KEYS = [0x0123, 0x4567, 0x89AB, 0xCDEF, 0xFEDC, 0xBA98]
EXPECTED_K6_NIBBLE = (ROUND_KEYS[5] >> ACTIVE_NIBBLE_SHIFT) & 0xF

TASK_DIRECTORY = Path(__file__).resolve().parent
DATA_DIRECTORY = TASK_DIRECTORY.parent / "code"
PLAINTEXT_FILE = DATA_DIRECTORY / "plaintext.txt"
CIPHERTEXT_FILE = DATA_DIRECTORY / "ciphertext.txt"


def read_data(filename):
    """读取以空格、逗号或换行分隔的16比特十六进制数据."""
    data = filename.read_text(encoding="utf-8").replace(",", " ").split()
    values = [int(value, 16) for value in data]

    if any(value < 0 or value >= STATE_SIZE for value in values):
        raise ValueError("输入文件中包含超出16比特范围的数据: %s" % filename)

    return values


def get_codebook():
    """读取明密文并建立明文到密文的一一对应关系."""
    plaintext = read_data(PLAINTEXT_FILE)
    ciphertext = read_data(CIPHERTEXT_FILE)

    if len(plaintext) != len(ciphertext):
        raise ValueError("明文和密文数量不一致.")

    codebook = dict(zip(plaintext, ciphertext))
    if len(codebook) != len(plaintext):
        raise ValueError("明文文件中存在重复值，无法建立一一对应的码本.")

    return codebook


def get_input_difference_pairs(codebook):
    """构造输入差分为0x0001的有序明文对及对应密文对."""
    ciphertext_pairs = []

    for plain_text_1, cipher_text_1 in codebook.items():
        plain_text_2 = plain_text_1 ^ INPUT_DIFFERENCE
        if plain_text_2 in codebook:
            cipher_text_2 = codebook[plain_text_2]
            ciphertext_pairs.append((cipher_text_1, cipher_text_2))

    return ciphertext_pairs


def denoise_pairs(ciphertext_pairs):
    """按密文差分筛选可能满足四轮目标差分的密文对."""
    selected_pairs = []

    for cipher_text_1, cipher_text_2 in ciphertext_pairs:
        difference = cipher_text_1 ^ cipher_text_2

        # 0x0010、0x0020、0x0050的其他半字节均为0.
        other_nibbles_are_zero = (difference & 0xFF0F) == 0
        active_difference = (difference >> ACTIVE_NIBBLE_SHIFT) & 0xF

        if (
            other_nibbles_are_zero
            and active_difference in ALLOWED_SBOX_OUTPUT_DIFFERENCES
        ):
            selected_pairs.append((cipher_text_1, cipher_text_2))

    return selected_pairs


def count_k6_nibble_candidates(selected_pairs):
    """枚举K6活动半字节的16种猜测并统计满足输入差分的次数."""
    counters = [0 for _ in range(16)]

    for cipher_text_1, cipher_text_2 in selected_pairs:
        nibble_1 = (cipher_text_1 >> ACTIVE_NIBBLE_SHIFT) & 0xF
        nibble_2 = (cipher_text_2 >> ACTIVE_NIBBLE_SHIFT) & 0xF

        for key_guess in range(16):
            input_1 = S_REVERSE[nibble_1 ^ key_guess]
            input_2 = S_REVERSE[nibble_2 ^ key_guess]

            if input_1 ^ input_2 == ACTIVE_NIBBLE_DIFFERENCE:
                counters[key_guess] += 1

    return counters


def main():
    """执行密文差分去噪并统计K6半字节候选."""
    codebook = get_codebook()
    ciphertext_pairs = get_input_difference_pairs(codebook)
    selected_pairs = denoise_pairs(ciphertext_pairs)
    counters = count_k6_nibble_candidates(selected_pairs)

    key_order = sorted(range(16), key=lambda key: (-counters[key], key))
    best_score = counters[key_order[0]]
    best_candidates = [key for key in key_order if counters[key] == best_score]
    expected_rank = key_order.index(EXPECTED_K6_NIBBLE) + 1

    print("输入差分: 0x%04X" % INPUT_DIFFERENCE)
    print("四轮目标差分: 0x%04X" % FOUR_ROUND_DIFFERENCE)
    print("输入差分明文对数: %d" % len(ciphertext_pairs))
    print("去噪后保留的明文对数: %d" % len(selected_pairs))
    print()
    print("K6活动半字节猜测 | 计数")
    print("----------------------")

    for key in key_order:
        print("       0x%X       | %d" % (key, counters[key]))

    print("----------------------")
    print("最高计数候选: %s" % ["0x%X" % key for key in best_candidates])
    print("参考密钥中K6对应半字节: 0x%X" % EXPECTED_K6_NIBBLE)
    print("参考半字节候选排名: %d/16" % expected_rank)


if __name__ == "__main__":
    main()
