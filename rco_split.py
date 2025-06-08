# rco_split.py
import random
from initial_solution import Route, euclidean

def split_path_rco(route, customers, id_to_index, L, p_bad=0.9, p_good=0.1):
    path = route.customers[1:-1]  # 去掉头尾 depot
    if len(path) < 2:
        return [route]

    segments = []
    current_segment = [path[0]]

    for i in range(1, len(path)):
        a = customers[id_to_index[path[i - 1]]]
        b = customers[id_to_index[path[i]]]
        dist = euclidean(a, b)

        prob = p_bad if dist > L else p_good
        if random.random() < prob:
            segments.append(current_segment)
            current_segment = [path[i]]
        else:
            current_segment.append(path[i])

    segments.append(current_segment)

    # 构造新Route对象，每段都加上 depot 头尾
    depot = customers[0]

    new_routes = []
    for seg in segments:
        if not seg:
            continue
        customer_ids = [depot.id] + seg + [depot.id]
        total_demand = sum(customers[id_to_index[cid]].demand for cid in seg)
        distance = 0.0
        for i in range(len(customer_ids) - 1):
            a = customers[id_to_index[customer_ids[i]]]
            b = customers[id_to_index[customer_ids[i + 1]]]
            distance += euclidean(a, b)

        new_routes.append(Route(customer_ids, total_demand, distance))

    return new_routes

def apply_rco_all(routes, customers, id_to_index):
    distances = []
    for route in routes:
        path = route.customers
        for i in range(len(path) - 1):
            a = customers[id_to_index[path[i]]]
            b = customers[id_to_index[path[i + 1]]]
            distances.append(euclidean(a, b))

    L = sum(distances) / len(distances) * 1.1  # 可调

    new_routes = []
    for route in routes:
        new_routes.extend(split_path_rco(route, customers, id_to_index, L))

    return new_routes
