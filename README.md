CVRP_HD_VNS/
 ├── data/                # 存放 Golden_1.vrp ~ Golden_20.vrp
 ├── sol/                 # 存放官方最优解 Golden_1.sol ~ Golden_20.sol
 ├── cvrp_parser.py       # VRP 文件解析模块
 ├── initial_solution.py  # 客户初始化路径生成模块
 ├── route_merge.py       # 初始路径合并模块
 ├── rco_split.py         # 路径切割（RCO）模块
 ├── hd_cluster.py        # 路径聚类与重构模块
 ├── vns_search.py        # 多邻域搜索（VNS）模块
 ├── batch_solver.py      # 主运行程序（单核）
 ├── results_summary.csv  # 实验结果汇总文件
