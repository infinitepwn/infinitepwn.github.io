import gurobipy as gp
import sys
from pathlib import Path

# 允许从任意工作目录直接运行
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ddt_lat import SIZE, bits, compute_ddt, compute_lat

def solve_one_hot(name, table, env):
    # DDT与LAT都取非零位置，包含全零传播以及LAT的负数表项。
    V = [(a, b) for a in range(SIZE) for b in range(SIZE) if table[a][b] != 0]

    with gp.Model(name, env=env) as model:
        # 八个原始变量的顺序为(a3,a2,a1,a0,b3,b2,b1,b0)。
        x = model.addVars(8, vtype=gp.GRB.BINARY)

        # 第一步：每个合法输入输出对对应一个二进制选择变量。
        lam = model.addVars(V, vtype=gp.GRB.BINARY)

        # 第二步：恰好选中一个合法点。
        model.addConstr(lam.sum() == 1)

        # 第三步：按坐标恢复所选点；只有该位为1的点对坐标和有贡献
        for j in range(8):
            model.addConstr(x[j] == gp.quicksum(lam[p] for p in V if bits(*p)[j] == 1))

        # 常数目标保留所有可行传播，不按概率或相关度筛选。
        model.setObjective(0, gp.GRB.MINIMIZE)
        model.Params.PoolSearchMode = 2
        # 八位点至多有2^8个，且每个点唯一确定lambda；容量取上界加1
        capacity = 2**8 + 1
        model.Params.PoolSolutions = capacity
        model.Params.MIPGap = 0
        model.Params.MIPGapAbs = 0
        model.optimize()

        # 这里只检查枚举是否完整，不与DDT/LAT进行结果比较。
        if model.Status != gp.GRB.OPTIMAL or model.SolCount >= capacity:
            raise RuntimeError(f"{name}未确认枚举完成，求解状态为{model.Status}。")

        # Gurobi13使用PoolNX，Gurobi12使用讲义中的Xn。
        attribute = "PoolNX" if hasattr(gp.GRB.Attr, "PoolNX") else "Xn"
        solutions = []
        for k in range(model.SolCount):
            model.Params.SolutionNumber = k
            values = [int(round(x[j].getAttr(attribute))) for j in range(8)]
            # 前四位还原输入，后四位还原输出；与公共模块的高位优先编码一致。
            a = sum(values[j] << (3 - j) for j in range(4))
            b = sum(values[j + 4] << (3 - j) for j in range(4))
            solutions.append((a, b))

        print(f"\n{name} one-hot：变量数={model.NumVars}，"
              f"等式数={model.NumConstrs}，解数={model.SolCount}")
        print("全部解（输入, 输出；十六进制）：")
        print(" ".join(f"({a:X},{b:X})" for a, b in sorted(solutions)))


if __name__ == "__main__":
    # 关闭Gurobi的过程日志，只保留上面的最终结果，也不设置任何日志文件。
    with gp.Env(empty=True) as env:
        env.setParam("OutputFlag", 0)
        env.start()
        solve_one_hot("DDT", compute_ddt(), env)
        solve_one_hot("LAT", compute_lat(), env)
