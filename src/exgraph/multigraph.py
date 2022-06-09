from exgraph.multidigraph import MultiDiGraph 
"""
This file solves section 1.
	1. Implementação de funções básicas para manipulação de grafos: 
		criar grafo, inserir arestas, inserir vértices,
		remover arestas, remover vértices, determinar o grau de um vértice,
		determinar se dois vértices são vizinhos, determinar se o grafo tem ciclo euleriano.		
"""

# Graph class, all operations are here
class MultiGraph(MultiDiGraph):
	# for a GND (NOT DIRECTED GRAPH) -> undirected=True, simple=True
	# V = Vertices, E = Edges, n = # of vertices
	def __init__(self,V,E,name="unnamed graph",*, weighted=False):
		super().__init__(V,E,name, weighted=weighted)
		self.out_deg 	= None
		self.in_deg 	= None

		self._isdirected = False
		for e in E:
			self.add_edge(tuple(e))

	"""@OVERRIDE"""
	# e = 2-tuple (u,v) \in E
	def add_edge(self,e):
		u,v = e[0],e[1]
		if self.isweighted:
			w = e[2]
			super().add_edge((u,v,w))
			super().add_edge((v,u,w))
		else:
			super().add_edge((u,v))
			super().add_edge((v,u))
			
	"""@OVERRIDE"""
	def remove_edge(self,e):
		u,v = e
		super().remove_edge((u,v))
		super().remove_edge((v,u))

	def weight(self,e) -> list[int] or None:
		if not self.weighted:
			return 1
		u,v = e
		if (u,v) in self._weights:
			return self._weights[(u,v)]
		
		elif (v,u) in self._weights:
			return self._weights[(v,u)]
		
		else:
			return None

	"""@OVERRIDE"""
	@property # m = |E| = Number of edges
	def m(self):
		# gotta divide by 2 because (a,b) == (b,a), so were counting twice
		return super().m/2 # GND and self is automatically passed to super()
	
	"""determinar o grau de um vértice"""
	def deg(self,v):
		return len(list(self.neighbours(v)))
