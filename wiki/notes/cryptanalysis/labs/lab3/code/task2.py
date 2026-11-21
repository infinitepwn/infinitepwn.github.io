"""
密码分析学第三次实验——任务二

基于题目表1.1给定的4比特S盒，计算LAT，寻找一轮可迭代的
16比特线性掩码固定点，并将其迭代4轮，计算单条路线的理论偏差。

注意：
1. 题目文档没有提供P层；此处采用课程参考程序的CipherFour转置置换。
2. 参考程序的S盒与实验题目不同，本文使用实验题目表1.1的S盒。
3. 输出的是单条线性路线的相关度/偏差，未计算线性包络(lin. hull)。
4. 轮密钥异或可能改变相关度的符号，但不改变其绝对值。

从仓库根目录运行：python3 labs/lab3/code/task2.py
"""

from fractions import Fraction

# 实验三题目表1.1的S盒（不是参考程序内的S盒）
SBOX = [
    0x9, 0x8, 0x0, 0x1,
    0xE, 0xB, 0xC, 0xD,
    0x3, 0x2, 0x5, 0x7,
    0xF, 0xA, 0x6, 0x4,
]

# 参考程序 3-练习 4.9.py 的CipherFour置换层。
# 采用从最高有效位(bit 15)到最低有效位(bit 0)的列表编号：
# new_bits[i] = old_bits[P_PERMUTATION[i]]
P_PERMUTATION = [
    0, 4, 8, 12,
    1, 5, 9, 13,
    2, 6, 10, 14,
    3, 7, 11, 15,
]

NIBBLES = 4
ROUND_COUNT = 4


def get_parity(value):
    """GF(2)内积中的奇偶性函数。"""
    return bin(value).count("1") % 2


def get_linear_table(sbox):
    """LAT[a][b] = #{x : <a,x>=<b,S(x)>} - 8。"""
    lat = [[0] * 16 for _ in range(16)]
    for alpha in range(16):
        for beta in range(16):
            equal_count = 0
            for x in range(16):
                p = get_parity(alpha & x)
                q = get_parity(beta & sbox[x])
                if p == q:
                    equal_count += 1
            lat[alpha][beta] = equal_count - 8
    return lat


def pass_linearphase(state):
    """对16比特状态/掩码施加与课程参考程序相同的P置换。"""
    result = 0
    for i, source_index in enumerate(P_PERMUTATION):
        bit = (state >> (15 - source_index)) & 1
        result |= bit << (15 - i)
    return result


def inverse_linearphase(mask):
    """逆P置换：已知P层之后的掩码，恢复P层之前的掩码。"""
    result = 0
    for i, source_index in enumerate(P_PERMUTATION):
        bit = (mask >> (15 - i)) & 1
        result |= bit << (15 - source_index)
    return result


def split_nibbles(mask):
    """从高到低返回4个4比特半字节掩码。"""
    return [(mask >> shift) & 0xF for shift in (12, 8, 4, 0)]


def get_round_correlation(alpha, beta, lat):
    """
    一轮S层的相关度：4个并行S盒的相关度之积。
    单S盒相关度C(a,b) = 2*LAT[a][b]/16 = LAT[a][b]/8。
    这里使用有理数精确计算。
    """
    result = Fraction(1)
    for a, b in zip(split_nibbles(alpha), split_nibbles(beta)):
        result *= Fraction(lat[a][b], 8)
        if result == 0:
            break
    return result


def search_iterative_linear_trail(lat):
    """
    枚举全部非零16比特输入掩码 alpha。
    为使每轮输入掩码保持相同，需要 P(beta) = alpha，
    因此 beta = P^{-1}(alpha)。

    对每个候选计算S层相关度，并按绝对相关度降序选出
    最强的「单轮固定点」迭代路线（不代表所有4轮路线的全局最优）。
    """
    candidates = []
    for alpha in range(1, 1 << 16):
        beta = inverse_linearphase(alpha)
        c = get_round_correlation(alpha, beta, lat)
        if c != 0:
            candidates.append((alpha, beta, c))

    if not candidates:
        raise RuntimeError("没有找到非零相关度的单轮迭代路线")

    # 绝对相关度相同，优先选择数值更大的输入掩码，使结果可重复。
    candidates.sort(key=lambda item: (-abs(item[2]), -item[0]))
    return candidates[0], candidates


def main():
    assert sorted(SBOX) == list(range(16)), "输入的S盒不是4比特置换"
    assert sorted(P_PERMUTATION) == list(range(16)), "P置换列表不合法"

    lat = get_linear_table(SBOX)
    assert lat[0][0] == 8
    assert all(sum(x * x for x in row) == 64 for row in lat), "LAT校验未通过"
    assert all(inverse_linearphase(pass_linearphase(1 << i)) == 1 << i
               for i in range(16)), "逆P置换校验未通过"

    (alpha, beta, c1), candidates = search_iterative_linear_trail(lat)
    epsilon1 = c1 / 2
    c4 = c1 ** ROUND_COUNT
    epsilon4 = c4 / 2

    print("=" * 68)
    print("任务二：CipherFour 四轮迭代线性路线搜索")
    print("=" * 68)
    print("S盒（实验题目表1.1）:", " ".join(f"{v:X}" for v in SBOX))
    print("P置换（课程参考程序）:", P_PERMUTATION)
    print("非零相关度的单轮固定点候选数量:", len(candidates))
    print()
    print("搜索得到的一条最优单轮固定点迭代路线：")
    print(f"  S层输入掩码 alpha = 0x{alpha:04X}")
    print(f"  S层输出掩码 beta  = 0x{beta:04X}")
    print(f"  P(beta)           = 0x{pass_linearphase(beta):04X}")
    print("  满足 P(beta) = alpha:", pass_linearphase(beta) == alpha)
    print()

    print("逐轮信息（4轮，每轮重复同一组S层掩码）：")
    for i in range(1, ROUND_COUNT + 1):
        print(f"  第{i}轮: 0x{alpha:04X} --S--> 0x{beta:04X} "
              f"--P--> 0x{pass_linearphase(beta):04X}; "
              f"C = {c1} ({float(c1):+.8f})")
    print()
    print("4轮输入掩码路线:")
    print("  " + " -> ".join([f"0x{alpha:04X}"] * (ROUND_COUNT + 1)))
    print()
    print("每个S盒的LAT贡献：")
    for j, (a, b) in enumerate(zip(split_nibbles(alpha), split_nibbles(beta)), 1):
        print(f"  S{j}: (a,b)=({a:X},{b:X}), "
              f"LAT[{a:X}][{b:X}]={lat[a][b]}, "
              f"C={Fraction(lat[a][b], 8)}")
    print()
    print(f"单轮相关度 C1      = {c1} = {float(c1):+.8f}")
    print(f"单轮偏差 epsilon1   = {epsilon1} = {float(epsilon1):+.8f}")
    print(f"4轮路线相关度 C4    = {c4} = {float(c4):+.8f}")
    print(f"4轮路线理论偏差    = {epsilon4} = {float(epsilon4):+.8f}")
    print(f"4轮路线绝对偏差    = {abs(epsilon4)} = {float(abs(epsilon4)):.8f}")
    print("注：轮密钥可能改变偏差符号；此处给出不含密钥符号因子的路线偏差。")
    print("注：单条路线的偏差不等于线性包络的总偏差。")


if __name__ == "__main__":
    main()
