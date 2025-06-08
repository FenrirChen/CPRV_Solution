# initial_solution.py
import math

class Route:
    def __init__(self, customers, total_demand, distance):
        self.customers = customers  # [1, i, 1]
        self.total_demand = total_demand
        self.distance = distance

def euclidean(p1, p2):
    return math.hypot(p1.x - p2.x, p1.y - p2.y)

def generate_initial_routes(customers):
    depot = customers[0]  # ID = 1
    routes = []

    for cust in customers[1:]:
        d1 = euclidean(depot, cust)
        d2 = euclidean(cust, depot)
        route = Route(customers=[depot.id, cust.id, depot.id],
                      total_demand=cust.demand,
                      distance=d1 + d2)
        routes.append(route)

    return routes
