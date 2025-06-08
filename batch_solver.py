import os
import time
import csv
import statistics

from cvrp_parser import parse_vrp_file
from initial_solution import generate_initial_routes
from rco_split import apply_rco_all
from hd_cluster import cluster_routes
from vns_search import vns_full_search
from route_merge import greedy_merge_routes


DATA_DIR = "data"
SOL_DIR = "sol"
CSV_FILE = "results_summary.csv"
RUNS = 20

def read_best_cost(sol_path):
    with open(sol_path, 'r') as f:
        for line in f:
            if line.lower().startswith("cost"):
                return float(line.strip().split()[-1])
    return None

def format_route(route):
    return "[" + " ".join(str(cid) for cid in route.customers) + "]"

with open(CSV_FILE, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        "Instance", "BestCost", "BestRoute", "WorstCost", "AvgCost", "StdDev",
        "RefBestCost", "AvgGap(%)"
    ])

    for i in range(1, 21):
        instance_name = f"Golden_{i}"
        vrp_path = os.path.join(DATA_DIR, f"{instance_name}.vrp")
        sol_path = os.path.join(SOL_DIR, f"{instance_name}.sol")
        print(f"[INFO] Processing {instance_name} for {RUNS} runs...")

        customers, capacity, id_to_index = parse_vrp_file(vrp_path)
        ref_best = read_best_cost(sol_path)

        all_costs = []
        all_routes = []

        for run in range(RUNS):
            run_start = time.time()
            init_routes_raw = generate_initial_routes(customers)
            init_routes = greedy_merge_routes(init_routes_raw, customers, id_to_index, capacity)

            rco_routes = apply_rco_all(init_routes, customers, id_to_index)
            clustered_routes = cluster_routes(rco_routes, customers, id_to_index, capacity)
            final_routes = vns_full_search(clustered_routes, customers, id_to_index, capacity)

            total_cost = sum(r.distance for r in final_routes)
            all_costs.append(total_cost)
            all_routes.append(final_routes)
            elapsed = time.time() - run_start  # ⏱ 停止计时
            print(f"[RUN {run + 1:02}/{RUNS}] {instance_name} finished: Cost={total_cost:.2f}, Time={elapsed:.2f}s")

        # 统计分析
        best_idx = all_costs.index(min(all_costs))
        best_cost = all_costs[best_idx]
        best_route = all_routes[best_idx]
        worst_cost = max(all_costs)
        avg_cost = statistics.mean(all_costs)
        stddev = statistics.stdev(all_costs)

        avg_gap = ((avg_cost - ref_best) / ref_best * 100) if ref_best else None

        # 格式化路径
        best_route_str = " | ".join(format_route(r) for r in best_route)

        writer.writerow([
            instance_name,
            f"{best_cost:.2f}",
            best_route_str,
            f"{worst_cost:.2f}",
            f"{avg_cost:.2f}",
            f"{stddev:.2f}",
            f"{ref_best:.2f}" if ref_best else "N/A",
            f"{avg_gap:.2f}%" if avg_gap is not None else "N/A"
        ])

        print(f"[DONE] {instance_name}: Best={best_cost:.2f}, Worst={worst_cost:.2f}, Avg={avg_cost:.2f}, Gap={avg_gap:.2f}%")

print(f"\n✅ All summary results saved to `{CSV_FILE}`")
