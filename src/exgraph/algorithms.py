from exgraph.graph import Graph as GND
from exgraph.digraph import DiGraph 
from exgraph.graph import _BaseGraph as IGraph
from collections import defaultdict, deque
from ds.unionfind import UnionFind

"""
This file solves section 2.
	2. Implementação do algoritmo de Hierholzer para determinação de uma cadeia euleriana fechada. 
"""
# INVERT THE ORDER OF THESE FUNCTIONS TO ENABLE OR DISABLE **DEBUGGING TEXT**
DEBUG = lambda info:print(info)
DEBUG = lambda info:False

#====================================================FUNCTIONS FOR ANY _BaseGraph==========================================================
# Helper function to print a path
def print_path(path:list, extra_msg=None):
	if extra_msg:
		print(f"\n{extra_msg}")
	if path:
		for v in range(len(path)-1):
			print(F"{path[v]}-",end="")
		print(f"{path[-1]}")	


#======================================================GND ALGORITHMS======================================================================
def is_cyclic(G:IGraph):
	path = set()
	def visit(v):
		path.add(v)
		for u in G.neighbours(v):
			if u in path or visit(v):
				return True
			path.remove(v)
		return False
	return any([visit(v) for v in G.V])
	
"""determinar se o grafo tem ciclo euleriano."""
# Function to determine GND is eulerian By Euler's Theorem
def is_eulerian(G:IGraph):
	if not is_connected(G):
		return False
	for v in G.V:
		if G.isdirected:
			if G.in_deg(v) != G.out_deg(v):
				DEBUG(f"graph:{G.name} is NOT EULERIAN, not all v in V has in_deg(v) == out_deg(v), v={v}")
				return False
		else:
			if not G.deg(v) % 2 == 0:
				DEBUG(f"graph:{G.name} is NOT EULERIAN, not all v in V has even deg(v), v={v}")
				return False
	# All deg's are even
	DEBUG(f"graph:{G.name} is EULERIAN ")
	return True


""""determinar se dois vértices são vizinhos"""
# G = graph, u,v ∈ V
def are_neighbours(G:GND,u,v):
	return v in G.neighbours(u) or u in G.neighbours(v)

# prints and returns the degree in sequence ex: 2,4,4,4,4,4
def degree_sequence(G:GND):
	sequence = list()
	for v in G.V:
		sequence.append(G.deg(v))
	DEBUG(f"graph {G.name} has sequence {sequence}")
	return sequence

def is_complete(G:GND):
	for v in G.V:
		for u in G.V:
			# if v is not the same vertices as u,
			# and does not have and edge between them, then is not complete
			if u != v and not are_neighbours(G,u,v):
				DEBUG(f"graph {G.name} is NOT complete")
				return False
	DEBUG(f"graph {G.name} is complete")
	return True

#Counting is all edges are n-1 deg Method
def is_complete_n(G:GND):
	for v in G.V:
		if G.deg(v) != G.n - 1:
			return False
	return True

def is_connected(G:GND):
	for v in G.V:
		visited_from_v = dfs(G,v)
		if set(G.V) != set(visited_from_v):
			DEBUG(f"graph {G.name} is NOT CONNECTED")
			return False
	DEBUG(f"graph {G.name} is CONNECTED")
	return True


#Depth First Search also return all visited nodes from v
#// DONE(Everton): use dfs_tree if you want all pathss
def dfs(G:GND,v):
	visited = set()
	def traversal(visited,G,node):
		if node not in visited:
			visited.add(node)
			for neighbour in G[node]:
				traversal(visited, G, neighbour)

	traversal(visited,G,v)
	return visited

# Hierholzer Algorithm
def hierholzer(G:IGraph):
	# check if has eulerian cicle
	if not is_eulerian(G):
		return False
	#===================Hierholzer=================
	path = []
	# Graph K with edges considered unvisisted, as we visit one edge 'e', we remove 'e'
	K = G.copy()

	# Pick any vertice 'v'
	v = next(K.V)	
	# While number of edges > 0
	deg = K.out_deg if K.isdirected else K.deg
	while K.m > 0:
		if deg(v) > 0:	
			# Next vertice
			u = next(K.neighbours(v))
			path.append(u)
			K.remove_edge((v,u))
			# current vertice is next vertice
			v = u
		else:
			# v equals the first element of the path
			v = path.pop(0)
			path.append(v)
	# At last we add the append the first element 
	# to the last turning the PATH into a CICLE
	return [*path,path[0]] 
		
	

        
#======================================================DIGRAPH ALGORITHMS======================================================================

def check_topological_order(G:DiGraph,L:list):
	assert(sorted(list(L)) == sorted(list(G.V)))
	for i,v in enumerate(L):
		p = G.predecessors(v)
		# para cada vertice w q que veio antes de v
		for w in L[:i]:
			# existe pelo menos 1 que está entre os predecessores de v
			if w in p:
				return True
	return False


def dfs_topsort(G:DiGraph):
	H = G.copy()
	# visitados
	visited = set()
	# L é a nossa ordenação topologica
	L = [] # topological order em L
	def traversal(visited,G:DiGraph,vertice):
		v = vertice
		# se v não foi visitado ainda
		if v not in visited:
			visited.add(v)
			# para cada arco sai do vertice v para w a gente visita w
			for w in G.neighbours(v):
				traversal(visited, G, w)
			# Quando terminou todas as visitas do vertice v
			# adicionamos v a L
			L.insert(0,v)

	# Diferente do Khan, não sabendo de cara qual são os vertices que não
	# há aresta incidente, por isso não há garantias que dado um vertice v
	# que iremos percorrer todo o grafo, portanto é necessario que façamos esse
	# loop de todos os v em H.V que não são visitados
	for v in H.V:
		if v not in visited:
			traversal(visited,H,v)
	return L

def khan_algorithm(G:DiGraph):
	H = G.copy()
	
	# Every single v in V that has none incident arcs
	S = [v for v in H.V if H.in_deg(v) == 0]
	# Ordenação topologica fica em L
	L = []

	while S != []:
		# remove v de S pelo começo, funciona como fila
		v = S.pop(0)
		# adiciona v ao final de L
		L.append(v)	

		arc_vw = list(H.neighbours(v))
		# para cada arco (v,w)
		for w in arc_vw:
			# removemos esse arco
			H.remove_edge((v,w))
			# se não tiver mais arcos incidentes adicionamos a S
			if H.in_deg(w) == 0:
				S.append(w)

	# Se as arestas de H não são vazias, decectamos um ciclo
	if list(H.E) != []:
		raise Exception(f"Digraph: {H.name} : id:{id(H)} has a cicle, and therefore cannot use khan's algorithm")
	return L

# Encontra caminho de v para w
# 1: path as a Path DiGraph
def tree2path(T:DiGraph,v,w ,*, tolist=False)-> DiGraph or list:
	if v not in T.V or w not in T.V: return Exception(f"Either vertices {v} or {w} not in V of the Tree {T.name}")

	P = DiGraph.empty(); P.name = f"Path {v}-...-{w}, from {T.name}"
	if tolist:
		path = deque([w])
	parent = None
	current = w
	while parent != v:
		# Supostamente deve ter apensar um predecessor
		parent = list( T.predecessors(current))[0]
		edge = (parent,current)
		if tolist:
			path.appendleft(parent)
		P.add_edge(edge)

		current = parent
	
	if tolist:
		return path
	return P


def dfs_tree(G:IGraph,v):
	
	#T = type(H).empty()
	# Resulting Tree
	T = DiGraph.empty()
	T.name = f"DFS Tree of {G.name} starting from {v}"
	# visitados
	visited = set()

	def traversal(G,v):
		nonlocal visited,T
		# adiciona v aos visitados
		visited.add(v)
		# para cada arco sai do vertice v para w a gente visita w
		for w in G.neighbours(v):
			#se w não for visitado ainda, o visitamos:
			if w not in visited:
				# adicionamos essa aresta a span-tree T
				T.add_edge((v,w))
				traversal(G, w)
			
	traversal(G,v)
	return T

def bfs_tree(G,v):
	# Tree with v as first vertice
	T = T = DiGraph.empty();T.add_vertice(v);T.name = f"DFS Tree of {G.name} starting from {v}"
	Q = deque() 		# Fila
	Q.append(v) 		#--v is inserted at the end of Q

	while len(Q) > 0: #-- While Q is not empty
		u = Q.popleft() 	#-- remove from beginning
		
		for w in G.neighbours(u):
			if w not in T.V and w not in Q:
				Q.append(w) 		#-- at the end
				T.add_edge((u,w)) #-- add edge vw to T
	return T

#/*=============================Weighted Graphs=========================================*/
def dijkstra (G:IGraph, s) -> dict:
	assert(s in G.V)
	dist = dict(); prev = dict()
	single_source_init(G, s,previous=prev,distance=dist)	
	
	C = set() 				#-- Closed C
	Q = set(G.V)			#-- Queue  Q
	T = DiGraph.empty(name=f"Dijkstra Tree from {G.name}")	#-- Tree T
	while Q: 	
		u =min(Q, key=lambda x:dist[x])
		Q.remove(u)
		C.add(u)
		T.add_edge((prev[u],u))
		for v in [vertice for vertice  in G[u] if vertice not in C]:
			w = G.weight((u,v))
			relax(u,v,w,previous=prev,distance=dist)
	return T


def bellman_ford_detect(G:IGraph,s):
	assert(s in G.V)
	dist = dict(); prev = dict()
	single_source_init(G, s,previous=prev,distance=dist)	
	for _ in range(G.n-1):
		for u,v in G.E:
			w = G.weight((u,v))
			relax(u,v,w,previous=prev,distance=dist)

	for u,v in G.E:
		w = G.weight((u,v))
		if dist[v] > dist[u] + w:
			return False
	return True

def bellman_ford(G:IGraph, s):
	assert(s in G.V)
	dist = dict(); prev = dict()
	single_source_init(G, s,previous=prev,distance=dist)	   
	for _ in range(G.n -1):
		for u,v in G.E:
			w = -G.weight((u,v))
			relax(u,v,w,previous=prev,distance=dist)
	return dist,prev

def single_source_init(G:IGraph, s,*,previous:dict,distance:dict):
	p = previous; d = distance
	for v in G.V:
		d[v] = float("inf")
		p[v] = None
	d[s] = 0
	p[s] = s
	
def relax(u,v,w,*,previous:dict,distance:dict):
	p = previous; d = distance
	if d[v] > d[u] + w:
		d[v] = d[u] + w
		p[v] = u

def prev2tree(previous):
	T = DiGraph.empty(name="Tree from previous set")
	for key in previous:
		T.add_edge((previous[key],key))
	return T


#/*================================ MST ======================================*/

def prims(G:IGraph,*,MST=None)  -> IGraph:
	# Se um buffer para a avore não for dada, criamos uma 
	T = DiGraph((),(),weighted=True) if MST is None else MST

	# Conjunto N que ira manter os vertices que ainda não fazem parte de T 
	N = set(G.V)
	# vertice i inicial
	i = next(G.V)

	# adicionamos i a T
	T.add_vertice(i)
	# removemos i a T
	N.remove(i)

	DEBUG.iteration = 0 
	DEBUG(f"iter {DEBUG.iteration}:")
	DEBUG(f"\tAresta inicial i ={i}")
	DEBUG(f"\tN = {N}")
	DEBUG(f"\tT.V = {T.V}")
	DEBUG("\tT.E = "+'{'+ ', '.join([f"({u},{v})" for u,v in T.E])+'}')
	DEBUG.iteration +=1

	weight_count = 0

	# Função que ira escolher a aresta de menor peso
	# entre todas as aresta (j,k) | j ∈ T.E e k ∈ N
	def choose_min():
		min_weight = float("inf")
		edge = None
		for j in T.V:
			for k in G.neighbours(j):
				if k not in N:
					continue
				w = G.weight((j,k)) 
				if w < min_weight:
					min_weight = w
					edge = (j,k)
		return edge,min_weight
	
	# Enquanto T ainda não possui todos os vertices
	while T.n != G.n:
		# Escolhemos o menor entre todas as aresta (j,k) | j ∈ T.E e k ∈ N
		(j,k),w = choose_min()
		DEBUG(f"iter {DEBUG.iteration}:");DEBUG(f"\tAresta min(T) = {(j,k)} com peso w={w}")
		
		# Peso total da avore é aumentado 
		weight_count += w
		# Adicionamos a MST e removemos de N e assim 
		# repetindo o ciclo de escolhas gananciosas/gulosa
		T.add_vertice(k)
		N.remove(k)
		T.add_edge((j,k,w))
		DEBUG(f"\tN = {N}")
		DEBUG(f"\tT.V = {T.V}")
		DEBUG("\tT.E = "+'{'+ ', '.join([f"({u},{v})" for u,v in T.E])+'}')

	DEBUG(f"Somatorios dos pesos dessa MST = {weight_count}")
	return T,weight_count

# T := Span Tree
# H := Vector of Edges Ordered by weight
def kruskal2(G:IGraph):
	H = sorted(list(G.E), key=G.weight)
	T = GND((),())
	wheight_count = 0
	
	T.add_edge(H[0])
	i = 1; j = 0
	while j < G.n-1:
		T.add_edge(H[i])
		if not is_cyclic(T): # aciclic:
			wheight_count += G.weight(H[i])
			j = j + 1
		else:
			T.remove_edge(H[i])
		i = i + 1
	
	return T

def kruskal(G:IGraph) -> IGraph:
	E = sorted(list(G.E), key=G.weight)
	MST = GND((),(),weighted=True)
	uf = UnionFind(list(G.V))
	DEBUG.iteration = 0 
	DEBUG("\tE = "+'{'+ ', '.join([f"({u},{v})" for u,v in E])+'}');
	weight_count = 0
	for u,v in E:
		w = G.weight((u,v))
		
		
		if uf.connected(u, v):
			#DEBUG(f"\t Não adicionamos essa aresta ({u},{v}), pois causaria cliclo")
			continue
		
		DEBUG(f"iter {DEBUG.iteration}:");  DEBUG.iteration += 1
		DEBUG("\tMST.E = "+'{'+ ', '.join([f"({u},{v})" for u,v in MST.E])+'}');
		DEBUG(f"\tAdicionamos ({u},{v}) a MST")
		MST.add_edge((u,v,w))
		uf.union(u, v)
		weight_count += w
	
	return MST,weight_count

#/*===================== APSP (all-pair-shortest-path) ================================*/

# NOT working
def floydwarshall(G:DiGraph):
	C = defaultdict(lambda x:float("inf"))
	for u,v in G.E:
		C[u,v] = G.weight((u,v))
	
	for v in G.V:
		C[v,v] = 0
	
	for k in range(G.n):
		for u in G.V:
			for v in G.V:
				pass

#/*================================ Matching ===============================*/

# This blossom's algorithms actually doenst allowed graphs that are not trees 
def blossom(G:IGraph,*,min=True) -> set:
	# Algoritmo de max-weight matching usando LP foi vendorizado de http://jorisvr.nl/article/maximum-matching
	from vendor.pmwmatching import maxWeightMatching as max_matching
	
	# max_matching espera um certo formado de edge que 
	# esta sendo coletado nesse for loop, e como queremos o 
	# min-matching, multiplicamos por -1 os pesos
	edges = set()
	for u,v in G.E:
		w  = G.weight((u,v))
		if (v,u) not in edges:
			if min:
				edges.add((u,v,-w))
			else:
				edges.add((u,v,w))

	# Encontramos o matching, talque match[i] = j se (i,j) é uma aresta 
	# que faz parte desse matching match[i] = -1  se não fizer parte
	match = max_matching(list(edges),maxcardinality=True) # O(n^3)
	
	perfect_matching = set()
	
	# Extraimos os matchings em formar de um tripla (i,j, w) onde w é o peso
	for i in range(len(match)):
		j = match[i]
		if j != -1:
			w = G.weight((i,j))
			# não queremos repetir edges
			if (j,i,w) not in perfect_matching:
				perfect_matching.add((i,j,w))
	return perfect_matching

# choosing min weight edge first then the next viable edge
def greedy_matching(G:IGraph) -> set:
	if not G.isweighted:
		raise Exception("Graph G is not weighted, <greedy_matching> expects a weighted graph")
	K = G.copy()
	M = set()
	while K.m != 0:
		min_edge 	= (-1,-1)
		min_weight 	= float("inf")
		
		for e in K.E:
			w = K.weight(e)
			try:
				w = w[0]
			except TypeError: 
				w = w
			if w <= min_weight:
				min_weight 	= w
				min_edge 	= (*e,w)

		M.add(min_edge)
		K.remove_vertice(min_edge[0])
		K.remove_vertice(min_edge[1])
	return M