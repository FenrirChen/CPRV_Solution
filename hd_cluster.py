import random
from sklearn.cluster import KMeans
from initial_solution import Route, euclidean

def compute_centroid(route, customers, id_to_index):
    # 使用路径中间点作为向量（简单版本）
    indices = route.customers[1:-1]
    if not indices:
        return [0, 0]
    x = sum(customers[id_to_index[cid]].x for cid in indices) / len(indices)
    y = sum(customers[id_to_index[cid]].y for cid in indices) / len(indices)
    return [x, y]

def cluster_routes(routes, customers, id_to_index, capacity, beta=0.1):
    # 1. 计算每个片段中心
    vectors = [compute_centroid(r, customers, id_to_index) for r in routes]

    max_k = max(1, int(beta * len(routes)))
    k = random.randint(1, max_k)

    # 2. 聚类
    kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
    labels = kmeans.fit_predict(vectors)

    clusters = [[] for _ in range(k)]
    for idx, r in enumerate(routes):
        clusters[labels[idx]].append(r)

    # 3. 每类内连接成合法路径（贪婪连接 + 满足容量限制）
    depot = customers[0]
    new_routes = []

    for group in clusters:
        current = [depot.id]
        total_demand = 0
        dist = 0.0

        # 将该类中所有客户逐个连接，超出容量就新建路径
        for r in group:
            for cid in r.customers[1:-1]:  # 跳过 depot
                demand = customers[id_to_index[cid]].demand
                if total_demand + demand > capacity:
                    # 封闭当前路径
                    current.append(depot.id)
                    # 计算距离
                    d = sum(euclidean(customers[id_to_index[current[i]]], customers[id_to_index[current[i+1]]]) for i in range(len(current)-1))
                    new_routes.append(Route(current, total_demand, d))
                    # 启动新路径
                    current = [depot.id, cid]
                    total_demand = demand
                else:
                    current.append(cid)
                    total_demand += demand

        # 封闭最后一条路径
        current.append(depot.id)
        d = sum(euclidean(customers[id_to_index[current[i]]], customers[id_to_index[current[i+1]]]) for i in range(len(current)-1))
        new_routes.append(Route(current, total_demand, d))

    return new_routes