"""任务一逐点排除法：建立模型、枚举并打印全部合法输入输出对。"""

import sys
from pathlib import Path

# 从任意工作目录运行时都能导入task1公共模块，并避免生成其字节码缓存。
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import gurobipy as gp
from ddt_lat import SIZE, bits, compute_ddt, compute_lat


def solve_point_exclusion(name, table, env):
    """逐个排除表中取值为0的点，保留所有非零点。"""
    # LAT的合法项包括正值和负值，因此只排除恰好为0的点。
    forbidden = [(a, b) for a in range(SIZE) for b in range(SIZE)
                 if table[a][b] == 0]

    with gp.Model(name, env=env) as model:
        # 八个二进制变量依次表示(a3,a2,a1,a0,b3,b2,b1,b0)。
        x = model.addVars(8, vtype=gp.GRB.BINARY)

        # 对每个非法点q添加汉明距离约束，要求当前点至少有一位不同于q。
        for point in forbidden:
            q = bits(*point)
            model.addConstr(gp.quicksum(
                x[j] if q[j] == 0 else 1 - x[j] for j in range(8)
            ) >= 1)

        # 常数目标保留全部可行点，不按概率或相关度筛选。
        model.setObjective(0, gp.GRB.MINIMIZE)
        model.Params.PoolSearchMode = 2
        # 八个二进制变量至多有2^8个点，容量取上界加1以确认解集完整。
        capacity = 2**8 + 1
        model.Params.PoolSolutions = capacity
        model.Params.MIPGap = 0
        model.Params.MIPGapAbs = 0
        model.optimize()

        # 只在Gurobi确认搜索完成后打印结果；不与其他方法自动比较。
        if model.Status != gp.GRB.OPTIMAL or model.SolCount >= capacity:
            raise RuntimeError(f"{name}未确认枚举完成，求解状态为{model.Status}。")

        # Gurobi13使用PoolNX，Gurobi12使用Xn读取解池中的第k个解。
        attribute = "PoolNX" if hasattr(gp.GRB.Attr, "PoolNX") else "Xn"
        solutions = []
        for k in range(model.SolCount):
            model.Params.SolutionNumber = k
            values = [int(round(x[j].getAttr(attribute))) for j in range(8)]
            # 前四位还原输入，后四位还原输出，位序与公共模块一致。
            a = sum(values[j] << (3 - j) for j in range(4))
            b = sum(values[j + 4] << (3 - j) for j in range(4))
            solutions.append((a, b))

        print(f"\n{name} 逐点排除：变量数={model.NumVars}，"
              f"约束数={model.NumConstrs}，解数={model.SolCount}")
        print("全部解（输入, 输出；十六进制）：")
        print(" ".join(f"({a:X},{b:X})" for a, b in sorted(solutions)))


if __name__ == "__main__":
    # 关闭Gurobi过程日志，打印上面的最终结果。
    with gp.Env(empty=True) as env:
        env.setParam("OutputFlag", 0) # 关闭Gurobi日志
        env.start()
        solve_point_exclusion("DDT", compute_ddt(), env)
        solve_point_exclusion("LAT", compute_lat(), env)
