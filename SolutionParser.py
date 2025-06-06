class SolutionParser:
    def read_solution_file(file_path):
        """解析 .sol 最优解文件，返回路线列表和目标成本"""
        routes = []
        total_cost = None
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith("Route"):
                    parts = line.split(':')
                    if len(parts) == 2:
                        customer_ids = list(map(int, parts[1].strip().split()))
                        routes.append(customer_ids)
                elif line.startswith("Cost"):
                    total_cost = float(line.split()[1])
        return routes, total_cost
    
    def calculate_gap(solution_cost, best_known_cost):
        """计算当前解与最优解之间的 GAP 百分比"""
        return 100.0 * (solution_cost - best_known_cost) / best_known_cost