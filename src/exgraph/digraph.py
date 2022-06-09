from typing import Iterable
from exgraph._basegraph import _BaseGraph 

class DiGraph(_BaseGraph):
	# for a DWG (DIRECTED WEIGHTED GRAPH)
	# V = Vertices, E = Edges, n = # of vertices
	def __init__(self,V:Iterable, E:tuple[any,any,int],*, name="unnamed DWG", weighted=False):
		W = None
		directed_edges = set()
		if weighted:
			W = dict[tuple,int]()

		for e in E:
			if weighted:
				u,v,weight = e
				W[(u,v)] = weight
			else:
				u,v = e
			directed_edges.add((u,v))
			
		super().__init__(V,directed_edges,name,W,directed=True)

	"""determinar quantidade de arcos que saem de v"""
	"""@OVERRIDE"""
	def out_deg(self,v):
		assert(v in self.V)
		return len(list(self.neighbours(v)))
	
	"""determinar quantidade de arcos incidentes em v"""
	"""@OVERRIDE"""
	def in_deg(self,v):
		assert(v in self.V)
		return len(list(self.predecessors(v)))
	

	# invert all directed edges
	def invert(self):
		for u,v in self.E:
			self.remove_edge(u,v)
			self.add_edge(v,u)
		return 