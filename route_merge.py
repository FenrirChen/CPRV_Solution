# route_merge.py
from initial_solution import euclidean, Route

def greedy_merge_routes(init_routes, customers, id_to_index, capacity):
    merged_routes = []
    visited = set()

    depot_id = customers[0].id

    while len(visited) < len(init_routes):
        # 找还未访问的第一个路径
        for i, route in enumerate(init_routes):
            if i not in visited:
                current = route.customers[1]  # 拿到该路径的唯一客户
                total_demand = route.total_demand
                path = [depot_id, current]
                visited.add(i)
                break

        while True:
            # 尝试找下一个最近邻客户并合并
            next_id = None
            min_dist = float('inf')

            for j, r in enumerate(init_routes):
                if j in visited:
                    continue
                candidate = r.customers[1]
                dist = euclidean(customers[id_to_index[current]], customers[id_to_index[candidate]])
                demand = customers[id_to_index[candidate]].demand
                if total_demand + demand <= capacity and dist < min_dist:
                    min_dist = dist
                    next_id = candidate
                    next_j = j

            if next_id is not None:
                path.append(next_id)
                total_demand += customers[id_to_index[next_id]].demand
                visited.add(next_j)
                current = next_id
            else:
                break

        path.append(depot_id)
        dist = sum(
            euclidean(customers[id_to_index[path[i]]], customers[id_to_index[path[i+1]]])
            for i in range(len(path) - 1)
        )
        merged_routes.append(Route(path, total_demand, dist))

    return merged_routes
