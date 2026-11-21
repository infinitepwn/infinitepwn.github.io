"""读取凸包H表示，贪心筛选不等式，并用Gurobi枚举合法点。"""

import json
import sys
from pathlib import Path

# 配置导入路径，复用task1中的表格计算与八位编码函数。
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import gurobipy as gp
from ddt_lat import SIZE, bits, compute_ddt, compute_lat


def linear_form(row, point):
    """按常数项在前的系数顺序计算c0+sum(cj*xj)。"""
    return row[0] + sum(coefficient * value
                        for coefficient, value in zip(row[1:], point))


def greedy_select(table, inequalities, equations):
    """保留全部等式，逐次选取能排除最多剩余非法点的不等式。"""
    forbidden = [bits(a, b) for a in range(SIZE) for b in range(SIZE)
                 if table[a][b] == 0]

    # 先移除已违反等式的点，其余非法点需要由不等式排除。
    remaining = {i for i, point in enumerate(forbidden)
                 if all(linear_form(row, point) == 0 for row in equations)}

    # 为每条候选不等式记录其排除的点；系数排序决定并列时的选择顺序。
    pool = {tuple(row): {i for i in remaining
                         if linear_form(row, forbidden[i]) < 0}
            for row in sorted(inequalities)}
    chosen = []
    while remaining:
        row = max(pool, key=lambda item: len(pool[item] & remaining),
                  default=None)
        if row is None or not (pool[row] & remaining):
            raise RuntimeError("凸包约束无法排除全部非法点，请检查JSON与当前S盒。")
        chosen.append(row)
        remaining.difference_update(pool.pop(row))
    return chosen


def solve_convex_hull(name, table, hrep, env):
    """把筛选后的H表示加入八位二进制模型，枚举并打印全部解。"""
    equations = hrep["equations"]
    chosen = greedy_select(table, hrep["inequalities"], equations)

    with gp.Model(name, env=env) as model:
        # 八个变量依次表示(a3,a2,a1,a0,b3,b2,b1,b0)。
        x = [model.addVar(vtype=gp.GRB.BINARY, name=f"x[{j}]")
             for j in range(8)]
        for row in equations:
            model.addConstr(linear_form(row, x) == 0)
        for row in chosen:
            model.addConstr(linear_form(row, x) >= 0)

        # 设置常数目标与解池搜索模式，枚举全部可行二进制点。
        model.setObjective(0, gp.GRB.MINIMIZE)
        model.Params.PoolSearchMode = 2
        capacity = 2**8 + 1
        model.Params.PoolSolutions = capacity
        model.Params.MIPGap = 0
        model.Params.MIPGapAbs = 0
        model.optimize()

        # 求解状态与解池容量共同确认枚举完成。
        if model.Status != gp.GRB.OPTIMAL or model.SolCount >= capacity:
            raise RuntimeError(f"{name}未确认枚举完成，求解状态为{model.Status}。")

        # Gurobi13使用PoolNX，Gurobi12使用Xn读取解池中的第k个解。
        attribute = "PoolNX" if hasattr(gp.GRB.Attr, "PoolNX") else "Xn"
        solutions = []
        for k in range(model.SolCount):
            model.Params.SolutionNumber = k
            values = [int(round(variable.getAttr(attribute))) for variable in x]
            # 前四位还原输入，后四位还原输出。
            a = sum(values[j] << (3 - j) for j in range(4))
            b = sum(values[j + 4] << (3 - j) for j in range(4))
            solutions.append((a, b))

        print(f"\n{name}凸包：原不等式数={len(hrep['inequalities'])}，"
              f"贪心保留不等式数={len(chosen)}，等式数={len(equations)}")
        print(f"变量数={model.NumVars}，约束数={model.NumConstrs}，"
              f"解数={model.SolCount}")
        print("全部解（输入, 输出；十六进制）：")
        print(" ".join(f"({a:X},{b:X})" for a, b in sorted(solutions)))


if __name__ == "__main__":
    data_path = Path(__file__).resolve().with_name("hull_constraints.json")
    if not data_path.is_file():
        raise FileNotFoundError("请先在WSL运行build_hull.py，生成hull_constraints.json。")
    hulls = json.loads(data_path.read_text(encoding="utf-8"))

    # 设置Gurobi环境的控制台日志开关。
    with gp.Env(empty=True) as env:
        env.setParam("OutputFlag", 0)
        env.start()
        solve_convex_hull("DDT", compute_ddt(), hulls["DDT"], env)
        solve_convex_hull("LAT", compute_lat(), hulls["LAT"], env)
