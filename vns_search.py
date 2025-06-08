import random
import copy
from initial_solution import euclidean, Route

def route_distance(route, customers, id_to_index):
    dist = 0.0
    for i in range(len(route) - 1):
        a = customers[id_to_index[route[i]]]
        b = customers[id_to_index[route[i + 1]]]
        dist += euclidean(a, b)
    return dist

# --- 算子1：单路径 - 单点插入
def intra_route_si(route: Route, customers, id_to_index):
    best = copy.deepcopy(route)
    best_cost = route.distance
    path = route.customers[1:-1]  # exclude depot

    for i in range(len(path)):
        for j in range(len(path)):
            if i == j:
                continue
            new_path = path[:]
            point = new_path.pop(i)
            new_path.insert(j, point)
            full_path = [route.customers[0]] + new_path + [route.customers[-1]]
            cost = route_distance(full_path, customers, id_to_index)
            if cost < best_cost:
                best = Route(full_path, route.total_demand, cost)
                best_cost = cost
    return best

# --- 算子2：Swap
def intra_route_swap(route: Route, customers, id_to_index):
    best = copy.deepcopy(route)
    best_cost = route.distance
    path = route.customers[1:-1]

    for i in range(len(path)):
        for j in range(i + 1, len(path)):
            new_path = path[:]
            new_path[i], new_path[j] = new_path[j], new_path[i]
            full_path = [route.customers[0]] + new_path + [route.customers[-1]]
            cost = route_distance(full_path, customers, id_to_index)
            if cost < best_cost:
                best = Route(full_path, route.total_demand, cost)
                best_cost = cost
    return best

# --- 算子3：2-opt
def intra_route_2opt(route: Route, customers, id_to_index):
    best = copy.deepcopy(route)
    best_cost = route.distance
    path = route.customers[1:-1]

    for i in range(len(path)):
        for j in range(i + 1, len(path)):
            new_path = path[:i] + path[i:j+1][::-1] + path[j+1:]
            full_path = [route.customers[0]] + new_path + [route.customers[-1]]
            cost = route_distance(full_path, customers, id_to_index)
            if cost < best_cost:
                best = Route(full_path, route.total_demand, cost)
                best_cost = cost
    return best

def inter_route_si(routes, customers, id_to_index, capacity):
    best_routes = copy.deepcopy(routes)
    improved = False

    for i in range(len(routes)):
        for j in range(len(routes)):
            if i == j:
                continue
            r1 = routes[i]
            r2 = routes[j]
            for idx in range(1, len(r1.customers) - 1):
                cust_id = r1.customers[idx]
                cust = customers[id_to_index[cust_id]]

                if r2.total_demand + cust.demand > capacity:
                    continue

                new_r1_path = r1.customers[:idx] + r1.customers[idx+1:]
                for insert_pos in range(1, len(r2.customers)):
                    new_r2_path = r2.customers[:insert_pos] + [cust_id] + r2.customers[insert_pos:]

                    d1 = route_distance(new_r1_path, customers, id_to_index)
                    d2 = route_distance(new_r2_path, customers, id_to_index)

                    if d1 + d2 < r1.distance + r2.distance:
                        new_r1 = Route(new_r1_path, r1.total_demand - cust.demand, d1)
                        new_r2 = Route(new_r2_path, r2.total_demand + cust.demand, d2)
                        best_routes[i] = new_r1
                        best_routes[j] = new_r2
                        improved = True
                        return best_routes, improved

    return routes, improved

# --- 路径间 Swap
def inter_route_swap(routes, customers, id_to_index, capacity):
    best_routes = copy.deepcopy(routes)
    improved = False

    for i in range(len(routes)):
        for j in range(i+1, len(routes)):
            r1 = routes[i]
            r2 = routes[j]

            for idx1 in range(1, len(r1.customers) - 1):
                for idx2 in range(1, len(r2.customers) - 1):
                    c1 = r1.customers[idx1]
                    c2 = r2.customers[idx2]
                    d1 = customers[id_to_index[c1]].demand
                    d2 = customers[id_to_index[c2]].demand

                    if (r1.total_demand - d1 + d2 > capacity) or (r2.total_demand - d2 + d1 > capacity):
                        continue

                    new_r1_path = r1.customers[:]
                    new_r2_path = r2.customers[:]
                    new_r1_path[idx1], new_r2_path[idx2] = c2, c1

                    d_new1 = route_distance(new_r1_path, customers, id_to_index)
                    d_new2 = route_distance(new_r2_path, customers, id_to_index)

                    if d_new1 + d_new2 < r1.distance + r2.distance:
                        new_r1 = Route(new_r1_path, r1.total_demand - d1 + d2, d_new1)
                        new_r2 = Route(new_r2_path, r2.total_demand - d2 + d1, d_new2)
                        best_routes[i] = new_r1
                        best_routes[j] = new_r2
                        improved = True
                        return best_routes, improved
    return routes, improved

# --- 主VNS流程（仅路径内 VNS）
def vns_full_search(routes, customers, id_to_index, capacity):
    improved = True
    while improved:
        improved = False
        # 路径内优化
        for idx, route in enumerate(routes):
            best = route
            for move in [intra_route_si, intra_route_swap, intra_route_2opt]:
                new_r = move(route, customers, id_to_index)
                if new_r.distance < best.distance:
                    best = new_r
                    improved = True
            routes[idx] = best

        # 路径间插入
        routes, flag1 = inter_route_si(routes, customers, id_to_index, capacity)
        # 路径间交换
        routes, flag2 = inter_route_swap(routes, customers, id_to_index, capacity)

        improved |= flag1 or flag2

    return routes