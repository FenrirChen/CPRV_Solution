import os
from Reading import Reading
from CVRP import CVRP
from SolutionParser import SolutionParser

def evaluate_all(data_dir):
    results = []
    for i in range(1, 21):
        vrp_file = os.path.join(data_dir, f"Golden_{i}.vrp")
        sol_file = os.path.join(data_dir, f"Golden_{i}.sol")

        # 读取 vrp 实例
        coords, demands, depot, capacity = Reading.read_vrp_file(vrp_file)
        problem = CVRP(coords, demands, capacity, depot)

        # 运行算法求解
        print(f"[INFO] Solving Golden_{i}...")
        my_routes, my_cost = problem.run()

        # 读取最优解并计算 GAP
        opt_routes, opt_cost = SolutionParser.read_solution_file(sol_file)
        gap = SolutionParser.calculate_gap(my_cost, opt_cost)

        print(f"Golden_{i}: My Cost = {my_cost:.2f}, Opt Cost = {opt_cost:.2f}, GAP = {gap:.2f}%")
        results.append((f"Golden_{i}", my_cost, opt_cost, gap))

    return results


def save_results(results, output_file="result/results.csv"):
    with open(output_file, 'w') as f:
        f.write("Instance,MyCost,OptCost,GAP(%)\n")
        for name, my_cost, opt_cost, gap in results:
            f.write(f"{name},{my_cost:.2f},{opt_cost:.2f},{gap:.2f}\n")

if __name__ == "__main__":
    data_folder = "./data"  # 请根据实际数据文件夹路径修改
    results = evaluate_all(data_folder)
    save_results(results)
    print("\n 所有数据处理完毕，结果已保存至 results.csv")