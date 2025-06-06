class Reading:
    def read_vrp_file(file_path):
        coords = {}
        demands = {}
        depot = None
        capacity = 0
        with open(file_path, 'r') as file:
            lines = file.readlines()

        section = None
        for line in lines:
            line = line.strip()
            if line.startswith("CAPACITY"):
                capacity = int(line.split(":")[1])
            elif line.startswith("NODE_COORD_SECTION"):
                section = "NODE"
                continue
            elif line.startswith("DEMAND_SECTION"):
                section = "DEMAND"
                continue
            elif line.startswith("DEPOT_SECTION"):
                section = "DEPOT"
                continue
            elif line == "EOF":
                break

            if section == "NODE" and len(line.split()) == 3:
                idx, x, y = line.split()
                coords[int(idx)] = (float(x), float(y))
            elif section == "DEMAND" and len(line.split()) == 2:
                idx, d = line.split()
                demands[int(idx)] = int(d)
            elif section == "DEPOT" and line != "-1":
                depot = int(line)

        return coords, demands, depot, capacity