# CVRP求解器主结构：混合遗传算法（Hybrid Genetic Algorithm, HGA）

import random
import math
import matplotlib.pyplot as plt


'''
初始化问题实例
coords  # 节点坐标字典 {节点ID: (x, y)}
demands  # 需求字典 {客户ID: 需求量}
capacity  # 车辆容量限制
depot  # 仓库节点ID（默认为1）
'''
class CVRP:
    def __init__(self, coords, demands, capacity, depot=1):
        self.coords = coords
        self.demands = demands
        self.capacity = capacity
        self.depot = depot
        self.n_customers = len(demands)  # 客户数量

    '''
    计算两个点之间的距离
    a:路径的起始点
    b.路径的终点
    '''
    def distance(self, a, b):
        x1, y1 = self.coords[a]
        x2, y2 = self.coords[b]
        return math.hypot(x1 - x2, y1 - y2)



    '''
    计算路径列表中的路径的总路径
    solution：路径列表
    '''
    def total_distance(self, solution):
        total = 0
        for route in solution:
            total += self.distance(self.depot, route[0])#从仓库节点结点0
            for i in range(len(route) - 1):
                total += self.distance(route[i], route[i+1])#从节点i到节点i+1
            total += self.distance(route[-1], self.depot)#从最后一个客户返回仓库
        return total


    '''
    检查路径是否符合容量的约束（即是否超载了）
    route:单条路径
    '''
    def is_feasible(self, route):
        return sum(self.demands[i] for i in route) <= self.capacity


    '''
    染色体切割
    chromosome；所有客户的排列
    '''
    def split_routes(self, chromosome):
        routes = []
        route = []
        load = 0
        for customer in chromosome:
            demand = self.demands[customer]
            if load + demand <= self.capacity:#如果目前负载+新需求为超出上限，则将此节点放入路径
                route.append(customer)
                load += demand
            else:#负载超出上限，将此路径放入路径集合，并将此客户放进下一条路径
                routes.append(route)
                route = [customer]
                load = demand
        if route:
            routes.append(route)
        return routes


    '''
    初始化种群
    pop_size：要求的种群大小
    '''
    def init_population(self, pop_size):
        population = []
        customers = list(self.demands.keys())
        customers.remove(self.depot)#去除掉种群中的仓库
        for _ in range(pop_size):
            chrom = customers[:]#复制客户列表
            random.shuffle(chrom)#随机排列客户列表
            population.append(chrom)#将新生成的染色体添加到种群中
        return population



    '''
    交叉繁殖产生子代
    parent1：父染色体
    parent2：母染色体
    '''
    def crossover(self, parent1, parent2):
        size = len(parent1)
        start, end = sorted(random.sample(range(size), 2))#无放回的抽样两次，得到切片的起始点和终止点
        child_p1 = parent1[start:end]
        child = [gene for gene in parent2 if gene not in child_p1]#筛选出母染色体中的“非父代切片”基因
        return child[:start] + child_p1 + child[start:]#插入父代切片完成交叉



    '''
    变异
    chrom：待变异的染色体
    '''
    def mutate(self, chrom):
        a, b = random.sample(range(len(chrom)), 2)#随机生成两个位置，交换这两个位置的基因
        chrom[a], chrom[b] = chrom[b], chrom[a]



    def local_search(self, routes):
        # 2-opt 局部搜索可选实现
        return routes

    '''
    主程序
    pop_size：种群大小，默认50
    generations：代数，默认200
    '''

    def run(self, pop_size=50, generations=200):
        population = self.init_population(pop_size)
        best_solution = None
        best_distance = float('inf')


        for gen in range(generations):
            scored = []
            '''
            评估种群
            '''
            for chrom in population:
                routes = self.split_routes(chrom)
                dist = self.total_distance(routes)
                scored.append((dist, chrom))
            scored.sort()
            best_candidate = scored[0]#当前轮次最优解
            if best_candidate[0] < best_distance:#如果优于全局最优解，则更新为全局最优解
                best_solution = best_candidate[1]
                best_distance = best_candidate[0]

            next_gen = [chrom for (_, chrom) in scored[:pop_size//4]]  # 精英保留25%
            while len(next_gen) < pop_size:
                p1, p2 = random.sample(scored[:pop_size//2], 2)#随机选择两个前50%的父代进行繁殖、变异
                child = self.crossover(p1[1], p2[1])
                if random.random() < 0.2:
                    self.mutate(child)
                next_gen.append(child)
            population = next_gen

        return self.split_routes(best_solution), best_distance

