from exgraph._basegraph import _BaseGraph 
"""
This file solves section 1.
	1. Implementação de funções básicas para manipulação de grafos: 
		criar grafo, inserir arestas, inserir vértices,
		remover arestas, remover vértices, determinar o grau de um vértice,
		determinar se dois vértices são vizinhos, determinar se o grafo tem ciclo euleriano.		
"""

# Graph class, all operations are here
class Graph(_BaseGraph):
	# for a GND (NOT DIRECTED GRAPH) -> undirected=True, simple=True
	# V = Vertices, E = Edges, n = # of vertices
	def __init__(self,V,E,name="unnamed graph",*, weighted=False):
		W = None
		undirected_edges = set()
		if weighted:
			W = dict[tuple,int]()
			
			for u,v,weight in E:
				undirected_edges.add((u,v))
				undirected_edges.add((v,u))
				W[(u,v)] = weight
				W[(v,u)] = weight
		else:
			for u,v in E:
				undirected_edges.add((u,v))
				undirected_edges.add((v,u))
			
		#super(_BaseGraph, self).__init__(V,undirected_edges,name,W)
		super().__init__(V,undirected_edges,name,W)

	"""@OVERRIDE"""
	# e = 2-tuple (u,v) \in E
	def add_edge(self,e):
		super().add_edge(e)
		# Because is undirected we must add vice-versa
		edge = [e[0],e[1]]
		if self.isweighted:
			edge.append(e[0])
		super().remove_edge(edge)

	"""@OVERRIDE"""
	def remove_edge(self,e):
		super().remove_edge(e)
		# Because is undirected we must remove the vice-versa
		# including from Weights, Edges and AdjList
		edge = [e[0],e[1]]
		if self.isweighted:
			edge.append(e[0])
		super().remove_edge(edge)
		


	"""@OVERRIDE"""
	@property # m = |E| = Number of edges
	def m(self):
		# gotta divide by 2 because (a,b) == (b,a), so were counting twice
		return super().m//2 # GND and self is automatically passed to super()
	
	"""determinar o grau de um vértice"""
	def deg(self,v):
		assert(v in self.V)
		if self.weighted:
			return sum([self.weight((v,u)) for u in self.neighbours(v)])
		return len(list(self.neighbours(v)))
