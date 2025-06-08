# cvrp_parser.py
import math

class Customer:
    def __init__(self, cid, x, y, demand):
        self.id = cid    # 原始ID（从1开始）
        self.x = x
        self.y = y
        self.demand = demand

def parse_vrp_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    node_section = False
    demand_section = False
    node_data = {}
    demand_data = {}

    for line in lines:
        if 'CAPACITY' in line:
            capacity = int(line.split()[-1])
        elif 'NODE_COORD_SECTION' in line:
            node_section = True
            continue
        elif 'DEMAND_SECTION' in line:
            node_section = False
            demand_section = True
            continue
        elif 'DEPOT_SECTION' in line or 'EOF' in line:
            demand_section = False
            break
        elif node_section:
            parts = line.strip().split()
            cid, x, y = int(parts[0]), float(parts[1]), float(parts[2])
            node_data[cid] = (x, y)
        elif demand_section:
            parts = line.strip().split()
            cid, demand = int(parts[0]), int(parts[1])
            demand_data[cid] = demand

    customers = []
    id_list = sorted(node_data.keys())  # 保证顺序一致
    for cid in id_list:
        x, y = node_data[cid]
        demand = demand_data[cid]
        customers.append(Customer(cid, x, y, demand))

    # 创建 ID 到索引映射（ID从1开始，索引从0开始）
    id_to_index = {cust.id: idx for idx, cust in enumerate(customers)}
    return customers, capacity, id_to_index
