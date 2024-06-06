import multiprocessing
import time

from project.cbip import execute_cbip
from project.first_fit import execute_first_fit
from project.graph_generator import generate_graphs

n_to_N = 1.35

def map_tasks(n):
    N = int(n * n_to_N)
    ratios_ff = []
    ratios_cbip = []
    for _ in range(N):
        k = 2
        graph = generate_graphs(k, 1, n)[0]
        ff = execute_first_fit(graph)
        ratios_ff.append(ff.get_competitive_ratio())
        ff = execute_cbip(graph)
        ratios_cbip.append(ff.get_competitive_ratio())
    avg_ff = round(sum(ratios_ff) / len(ratios_ff), 3)
    print(f"ff,{k},{N},{n},{avg_ff}")
    avg_cbip = round(sum(ratios_cbip) / len(ratios_cbip), 3)
    print(f"cbip,{k},{N},{n},{avg_cbip}")


if __name__ == '__main__':
    start = time.time()
    print("algo,k,N,n,avg")
    p = multiprocessing.Pool(multiprocessing.cpu_count() - 1)
    p.map(map_tasks, [x for x in range(50, 1650, 50)])
    p.close()
    p.join()
    print("time: ", round(time.time() - start, 2))
