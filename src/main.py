from tspheuristics import christofides,twice_around,bellmore_nemhauser,insert_vertice_1,insert_vertice_2
import tspgraphs
from exgraph.graph 	import Graph
from utils import measure

# Nome para o arquivo onde todas as info sobre as heuristicas vão
INFO_FILE_NAME = "TSP Heuristic Tours Info"

# calcula custo de um caminho
def path_cost(G:Graph, path:list):
	p = iter(path)
	total_cost = 0

	v = next(p)
	for u in p:
		e = (v, u)
		w = G.weight(e)
		total_cost += w
		v = u
	return total_cost

# Escreve TSP info (solução, custo) sobre um grafo + heuristica 
def tsp_test(G,fn,filename):
	H = fn(G)
	heuristic = fn.__name__
	out = list()
	exec_time = measure(path_cost,G,H,out=out)
	cost = out[0]
	#cost = path_cost(G,H)
	info = f"""
>---------------------------------------------------
Graph: {G.name}, |V| = {G.n}, |E| = {G.m}
Heuristic: {heuristic}
Tour: {H}
{exec_time:.7f}s execution time
{float(cost)} cost using heuristic {heuristic}
{float(G.tsp_min)} cost of best path
{cost/G.tsp_min:.4f} ratio {heuristic}/best
<---------------------------------------------------\n
"""
	with open(filename, mode='a') as f:
		f.write(info)
	print(info)

def __main__():
	# Clear info text about heuristics

	heuristics = [
		bellmore_nemhauser,
		twice_around,
		christofides,
		insert_vertice_1,
		insert_vertice_2
	]
	
	graphs = [
		tspgraphs.ATT48(),
		tspgraphs.FIVE(),
		tspgraphs.DANTZIG42(),
		tspgraphs.FRI26(),
		tspgraphs.P01(),
	]

	for fn in heuristics: 
		filename = INFO_FILE_NAME + f" {fn.__name__}.txt"
		open(filename, mode='w').close()
		for G in graphs:
			tsp_test(G,fn,filename)


if __name__ == '__main__':
	__main__()