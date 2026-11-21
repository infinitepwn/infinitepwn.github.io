"""任务一逻辑化简法：Espresso化简非法点，再由Gurobi枚举合法点。"""

import sys
from pathlib import Path

# 从任意工作目录运行时都能导入task1公共模块，并避免生成其字节码缓存。
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import gurobipy as gp
from pyeda.boolalg.bfarray import exprvars
from pyeda.boolalg.expr import And, Or
from pyeda.boolalg.minimization import espresso_exprs

from ddt_lat import SIZE, bits, compute_ddt, compute_lat


def simplify_forbidden_points(table):
    """用Espresso把表中所有零值位置化简成含通配位的立方体。"""
    variables = exprvars("x", 8)
    minterms = []

    # 以每个零值位置构造一个最小项，组成“非法点函数”的析取范式。
    for a in range(SIZE):
        for b in range(SIZE):
            if table[a][b] == 0:
                point = bits(a, b)
                minterms.append(And(*(
                    variable if value else ~variable
                    for variable, value in zip(variables, point)
                )))

    # Espresso合并相邻最小项；输出函数仍表示同一组非法点。
    forbidden_function = Or(*minterms).to_dnf()
    minimized, = espresso_exprs(forbidden_function)

    # 每个立方体是一组文字；未出现的变量就是通配位，用None标记。
    variable_index = {variable.uniqid: j
                      for j, variable in enumerate(variables)}
    cubes = []
    for term in minimized.to_dnf().cover:
        cube = [None] * 8
        for literal in term:
            literal_id = literal.uniqid
            j = variable_index[abs(literal_id)]
            cube[j] = int(literal_id > 0)
        cubes.append(cube)
    return cubes


def solve_logic_minimization(name, table, env):
    """将每个非法点立方体转成排除约束，并枚举所有剩余点。"""
    cubes = simplify_forbidden_points(table)

    with gp.Model(name, env=env) as model:
        # 八个二进制变量依次表示(a3,a2,a1,a0,b3,b2,b1,b0)。
        x = model.addVars(8, vtype=gp.GRB.BINARY, name="x")

        # 对每个立方体，要求至少一个固定文字取反，从而排除该立方体。
        for cube in cubes:
            model.addConstr(gp.quicksum(
                x[j] if value == 0 else 1 - x[j]
                for j, value in enumerate(cube) if value is not None
            ) >= 1)

        # 常数目标保留所有可行点，不按概率或相关度筛选。
        model.setObjective(0, gp.GRB.MINIMIZE)
        model.Params.PoolSearchMode = 2
        # 八个二进制变量至多有2^8个点，容量取上界加1以确认解集完整。
        capacity = 2**8 + 1
        model.Params.PoolSolutions = capacity
        model.Params.MIPGap = 0
        model.Params.MIPGapAbs = 0
        model.optimize()

        # 在Gurobi确认搜索完成后打印结果。
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

        print(f"\n{name} 逻辑化简：变量数={model.NumVars}，"
              f"约束数={model.NumConstrs}，解数={model.SolCount}")
        print("全部解（输入, 输出；十六进制）：")
        print(" ".join(f"({a:X},{b:X})" for a, b in sorted(solutions)))


if __name__ == "__main__":
    # 关闭Gurobi过程日志，只打印上面的最终结果，不生成日志或结果文件。
    with gp.Env(empty=True) as env:
        env.setParam("OutputFlag", 0)
        env.start()
        solve_logic_minimization("DDT", compute_ddt(), env)
        solve_logic_minimization("LAT", compute_lat(), env)
