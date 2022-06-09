import os
from os.path import exists
from exgraph.graph import Graph
from utils import txt2list as text2list

#exists = lambda x:False

# Transforma um txt de pesos para um grafo com vertice enumerados com inteiros
def _weight_text2graph(folder:str, graph_name:str):
	filepath = os.path.join(f'data/{folder}/', f'{graph_name}.graph')

	# Se o grafo já fora salvo usando pickle, então carregamos ele da memoria
	if exists(filepath):
		return Graph.load(filepath)
	
	# Senão, devemos pegar a matrix desse .txt
	weight_matrix 	= text2list(f"{graph_name}_d.txt",	fn=lambda x:[float(i) for i in x.split()])
	n = len(weight_matrix)
	
	# Creating weighted graph
	G = Graph((),(),weighted=True, name=graph_name)
	
	# Adiciona os edges a partir da matriz
	for i in range(n):
		for j in range(n):
			if j == i: continue
			weight = weight_matrix[i][j]
			G.add_edge((i+1,j+1,weight))
	return G

# Cria e retorna o grafo att48
def ATT48() -> Graph:
	name 		= "att48"
	folder 	= "ATT48"
	filepath = os.path.join(f'data/{folder}/', f'{name}.graph')

	if exists(filepath):
		return Graph.load(filepath)
	
	G = _weight_text2graph(folder, name)

	coord 		= text2list("att48_xy.txt",fn=lambda x:[float(i) for i in x.split()])
	tsp_path 	= text2list("att48_s.txt",	fn=lambda x:int(x))

	G.coord 		= coord
	G.tsp_path 	= tsp_path
	G.tsp_min 	= 33523
	G.save(filepath)
	return G

# Cria e retorna o grafo dantzig42
def DANTZIG42() -> Graph:
	name 		= "dantzig42"
	folder 	= "DANTZIG42"
	filepath = os.path.join(f'data/{folder}/', f'{name}.graph')
	if exists(filepath):
		return Graph.load(filepath)
	
	G = _weight_text2graph(folder, name)

	start_of_coord = False
	def filter_coord(line:str):
		nonlocal start_of_coord
		if line == "EOF":
			return None
		if line == "DISPLAY_DATA_SECTION\n":
			start_of_coord = True
			return None
		if start_of_coord:
			line = line.split()
			return line[1:]
			
	coord 		= text2list("dantzig42.tsp",	 fn=filter_coord)
	
	G.coord 		= coord
	G.tsp_min 	= 699

	G.save(filepath)
	return G


# Cria e retorna o grafo five
def FIVE() -> Graph:
	name 		= "five"
	folder 	= "FIVE"
	filepath = os.path.join(f'data/{folder}/', f'{name}.graph')

	if exists(filepath):
		return Graph.load(filepath)
	
	G = _weight_text2graph(folder, name)

	tsp_path 	= text2list(f"{name}_s.txt",	fn=lambda x:int(x))

	G.tsp_path 	= tsp_path
	G.tsp_min 	= 19
	G.save(filepath)
	
	return G
	
	
# Cria e retorna o grafo fri26
def FRI26() -> Graph:
	name 		= "fri26"
	folder 	= "FRI26"
	filepath = os.path.join(f'data/{folder}/', f'{name}.graph')

	if exists(filepath):
		return Graph.load(filepath)
	
	G = _weight_text2graph(folder, name)

	tsp_path 	= text2list(f"{name}_s.txt",	fn=lambda x:int(x))

	G.tsp_path 	= tsp_path
	G.tsp_min 	= 937
	G.save(filepath)
	
	return G
	
	
# Cria e retorna o grafo gri17
def GR17() -> Graph:
	name 		= "gr17"
	folder 	= "GR17"
	filepath = os.path.join(f'data/{folder}/', f'{name}.graph')

	if exists(filepath):
		return Graph.load(filepath)
	
	G = _weight_text2graph(folder, name)

	tsp_path 	= text2list(f"{name}_s.txt",	fn=lambda x:int(x))

	G.tsp_path 	= tsp_path
	G.tsp_min 	= 2085
	G.save(filepath)
	
	return G


# Cria e retorna o grafo p01
def P01() -> Graph:
	name 		= "p01"
	folder 	= "P01"
	filepath = os.path.join(f'data/{folder}/', f'{name}.graph')

	if exists(filepath):
		return Graph.load(filepath)
	
	G = _weight_text2graph(folder, name)

	tsp_path 	= text2list(f"{name}_s.txt",	fn=lambda x:int(x))

	G.tsp_path 	= tsp_path
	G.tsp_min 	= 291
	G.save(filepath)
	
	return G

# Exemplo do livro Grafos - Marco Goldbard pag. 551
def SIX() -> Graph:
	name 		= "six"
	folder 	= "SIX"
	filepath = os.path.join(f'data/{folder}/', f'{name}.graph')

	if exists(filepath):
		return Graph.load(filepath)
	
	E = {
		(1,2, 1), (1,3, 4), (1,4, 9), (1,5, 8), (1,6, 2),
		(2,3, 5), (2,4, 5), (2,5, 7), (2,6, 6),
		(3,4, 10),(3,5, 10),(3,6, 4),
		(4,5, 1), (4,6, 7),
		(5,6, 3)
	}
	G = Graph(V={i+1 for i in range(6)}, E=E,weighted=True)

	G.tsp_min 	= 31
	G.save(filepath)
	return G
