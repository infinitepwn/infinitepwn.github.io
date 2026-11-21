"""
密码分析学第三次实验——第三题

PHILOX-2W 一轮线性掩码传播分析

实验参数：
    W = 8
    M = 0x9B

输入掩码：
    (0,1), (1,0), (0,2), (2,1)

实验目标：
    对每个输入掩码，计算所有输出掩码对应的线性偏差，
    输出绝对偏差最大的前5个输出掩码及其偏差。
"""

# ============================================================
# 1. 参数定义
# ============================================================

W = 8
M = 0x9B
K = 0x00

N = 1 << W
MASK = N - 1

input_masks = [
    (0x00, 0x01),
    (0x01, 0x00),
    (0x00, 0x02),
    (0x02, 0x01)
]


# ============================================================
# 2. 基础函数
# ============================================================

def get_parity(value):
    """
    计算整数中1的个数的奇偶性。

    返回：
        0：偶数个1
        1：奇数个1
    """
    return bin(value).count("1") % 2


def philox_round(L, R, K=0):
    """
    PHILOX-2W 一轮加密。

    L' = mullo(R)
    R' = mulhi(R) XOR L XOR K
    """

    product = R * M

    mullo = product & MASK
    mulhi = (product >> W) & MASK

    L_next = mullo
    R_next = mulhi ^ L ^ K

    return L_next, R_next


# ============================================================
# 3. 计算一轮线性偏差
# ============================================================

def get_linear_bias(alpha, beta):
    """
    计算输入掩码alpha到输出掩码beta的线性偏差。

    alpha = (alpha_L, alpha_R)
    beta  = (beta_L, beta_R)

    线性关系：

        alpha_L·L XOR alpha_R·R
        =
        beta_L·L' XOR beta_R·R'

    偏差：

        epsilon = P[线性关系成立] - 1/2

    利用PHILOX轮函数：

        L' = mullo(R)
        R' = mulhi(R) XOR L XOR K

    代入得到：

        (alpha_L XOR beta_R)·L
        XOR alpha_R·R
        XOR beta_L·mullo(R)
        XOR beta_R·mulhi(R)
        XOR beta_R·K = 0

    当alpha_L != beta_R时，
    由于L均匀分布，线性偏差必为0。

    当alpha_L == beta_R时，
    只需遍历R的256种取值。
    """

    alpha_L, alpha_R = alpha
    beta_L, beta_R = beta

    # Feistel结构的掩码传播条件
    if alpha_L != beta_R:
        return 0.0

    equal_count = 0

    # 遍历全部256种R
    for R in range(N):

        product = R * M

        mullo = product & MASK
        mulhi = (product >> W) & MASK

        # 输入掩码对应的内积
        input_parity = get_parity(alpha_R & R)

        # 输出掩码对应的内积
        output_parity = (
            get_parity(beta_L & mullo)
            ^ get_parity(beta_R & mulhi)
            ^ get_parity(beta_R & K)
        )

        if input_parity == output_parity:
            equal_count += 1

    # 计算线性偏差
    bias = equal_count / N - 0.5

    return bias


# ============================================================
# 4. 搜索输出掩码
# ============================================================

def search_output_masks(alpha):
    """
    对指定输入掩码alpha，
    搜索绝对偏差最大的前5个输出掩码。

    根据Feistel结构：
        beta_R = alpha_L

    因此只需枚举beta_L的256种取值。
    """

    alpha_L, alpha_R = alpha

    results = []

    # 枚举输出左分支掩码
    for beta_L in range(N):

        # 输出右分支掩码由传播条件确定
        beta_R = alpha_L

        # 排除全零输出掩码
        if beta_L == 0 and beta_R == 0:
            continue

        beta = (beta_L, beta_R)

        # 计算线性偏差
        bias = get_linear_bias(alpha, beta)

        results.append(
            (beta_L, beta_R, bias)
        )

    # 按绝对偏差从大到小排序
    # 绝对偏差相同时，按掩码数值升序排列
    results.sort(
        key=lambda x: (
            -abs(x[2]),
            x[0],
            x[1]
        )
    )

    return results[:5]


# ============================================================
# 5. 输出实验结果
# ============================================================

def print_results():

    print("=" * 75)
    print("PHILOX-2W 一轮线性掩码传播分析")
    print("=" * 75)

    print(f"W = {W}")
    print(f"M = 0x{M:02X}")
    print(f"K = 0x{K:02X}")

    for alpha in input_masks:

        results = search_output_masks(alpha)

        print("\n" + "-" * 75)

        print(
            f"输入掩码 alpha = "
            f"(0x{alpha[0]:02X}, 0x{alpha[1]:02X})"
        )

        print("-" * 75)

        print(
            f"{'Rank':<8}"
            f"{'Output Mask':<22}"
            f"{'Bias':<18}"
            f"{'Absolute Bias':<18}"
        )

        for i, (beta_L, beta_R, bias) in enumerate(
            results, start=1
        ):

            print(
                f"{i:<8}"
                f"(0x{beta_L:02X}, 0x{beta_R:02X})      "
                f"{bias:+.8f}       "
                f"{abs(bias):.8f}"
            )

    print("\n" + "=" * 75)
    print("全部输入掩码分析完成！")
    print("=" * 75)


# ============================================================
# 6. 主函数
# ============================================================

if __name__ == "__main__":

    print_results()