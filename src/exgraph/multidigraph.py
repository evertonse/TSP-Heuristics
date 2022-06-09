from ds.multiset import MultiSet

EdgesContainer 		= MultiSet
NeighboursContainer 	= MultiSet
WeightsContainer		= dict[MultiSet,list[int]]
VerticesContainer 	= set

Edge = tuple

from typing import Iterable

# MultiGraph class, all operations are here
class MultiDiGraph():	
	@classmethod
	def empty(cls,*,name="empty"):
		return cls((),(),name=name)

	# for a MultiGraph (DIRECTED MultiGraph) ->
	# V = Vertices, E = Edges, n = # of vertices, if 
	def __init__(self,V,E,name="unnamed graph",*, weighted=False):
		# set name of the graph
		self.name		  = name
		self._isweighted = weighted
		self._isdirected = True
		
		self._weights 	= WeightsContainer()
		self._edges 	= EdgesContainer()
		"""utilizar listas de adjacências"""
		self._adj_list = {v:NeighboursContainer() for v in V}	
		
		"""utilizar listas de predecessores"""
		self._pred_list = {v:NeighboursContainer() for v in  V}	
		
		for v in V:
			self.add_vertice(v)
		for e in E:
			self.add_edge(tuple(e))

	"""inserir arestas"""
	# e = 2-fset {u,v} ∈ E
	def add_edge(self,e):
		if e[0] not in self.V:
			self.add_vertice(e[0])
		if e[1] not in self.V:
			self.add_vertice(e[1])

		# Because is directed we must NOT add vice-versa
		# Must only add once
		edge = (e[0],e[1])
		self._edges.add(edge)
		
		self._adj_list[e[0]].add(e[1])
		self._pred_list[e[1]].add(e[0])
		
		if self.weighted:
			weight = e[2]
			if edge not in self._weights:
				self._weights[edge] = list()
			self._weights[edge].append(weight)

	"""inserir vértices"""
	def add_vertice(self,v):
		if v not in self._adj_list:
			self._adj_list[v] 	= NeighboursContainer()
			self._pred_list[v] 	= NeighboursContainer()

	"""remover arestas"""
	def remove_edge(self,e):
		edge = tuple(e)			
		if edge not in self._edges:
			return
		if self.weighted:
			self.W[edge].remove(next(iter(self.W[edge])))
			if len(self.W[edge]) == 0:
				del(self.W[edge])
				
		self._edges.remove(edge)

		self._adj_list[e[0]].remove(e[1])
		self._pred_list[e[1]].remove(e[0])


	""""remover vértices"""
	def remove_vertice(self,v):
		for u in list(self.neighbours(v)):
			e = (v,u)
			self.remove_edge(e)
		for u in list(self.predecessors(v)):
			e = (u,v)
			self.remove_edge(e)
		del(self._adj_list[v])
		del(self._pred_list[v])


	def copy(self):
		CurrentClass = type(self) 
		C = CurrentClass((),(),name=f"{self.name} copy",weighted=self.isweighted)
		# Don't need to worry about if its directed or not, because each type 
		# will deal with add_edge is the proper way, we only care if it is weighted or not
		# because that will actually change the expecting value in add_edge 
		# method from 2-tuple -> u,v to a 3-tuple -> u,v and weight
		for e in self.E:
			if C.weighted:
				w = self.weight(e)
				C.add_edge((*e,w[0]))
			else:
				C.add_edge(e)
		return C

	def weight(self,e) -> list[int] or None:
		if e not in self._weights: 
			return None
		if self.weighted:
			return self._weights[e]
		else:
			return 1

	def distance(self,p:Iterable):
		if not self.weighted: return len(p)
		total = 0
		for i in range(len(p)-1):
			e = (p[i],p[i+1])
			total += self.weight(e)
		return total

	@property
	def weighted(self):
		return self._isweighted
	@property
	def isweighted(self):
		return self._isweighted
	@property
	def isdirected(self):
		return self._isdirected
		
	@property
	def W(self):
		return self._weights
		
	@property # E = Edges
	def E(self):
		return iter(self._edges)
	
	@property # n = |V| =  Number of vertices
	def n(self):
		return sum([1 for i in self.V])
	
	@property # m = |E| = Number of edges
	def m(self):
		# gotta divide by 2 because (a,b) == (b,a), so were counting twice
		return sum([1 for i in self.E])

	@property # V = Vertices
	def V(self):
		return iter(self._adj_list.keys())

 	#// TODO(Everton): Implement random vertice efficiently
	def any_vertice(self):
		from random import randint
		rand_index = randint()
		return NotImplemented

	def neighbours(self,v):
		# returns a ITERABLE of neighbours
		return iter(self._adj_list[v])

	def predecessors(self,v):
		# returns a ITERABLE of predecessors
		return iter(self._pred_list[v])

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
	
	# PRINT some useful information about this graph
	def print(self,sort=False,slim=True,tofile=False):
		print(self.__repr__(sort=sort))
		if tofile:
			import os
			folder = "./graphs_repr/"
			os.makedirs(os.path.dirname(folder), exist_ok=True)
			with open(f'{folder}{self.name}.txt','w') as f:
				f.write(self.__repr__(sort=sort,slim=slim))
			print(f"graph saved with sucess at: {folder}{self.name}.txt")
		
#/*=====================================DUNDERS=================================*/
	def __repr__(self, sort=False,slim=True):
		V = list(self.V)
		if sort == True:
			ordered = sorted
			V = sorted(list(self.V))
		else:
			ordered = lambda x:x		
		result =f"__________________{self.__class__.__name__}:{self.name}_______________________\n"
		if self.weighted:
			result += f"{self.name}\nGraph-Type Wheighted:{type(self)}\n"
		else:
			result += f"{self.name}\nGraph-Type:{type(self)}\n"
		
		for v in V:
			if self.weighted:
				result += f"{v}->{ordered([f'{u}|{self.W[(u,v)]}' for u in list(self.neighbours(v))])}"+ "\n"
			else:
				result += f"{v}->{ordered(list(self.neighbours(v)))}"+ "\n"
		if not slim:
			result += f"\nVertices:\n {V}\n"
			result += f"Edges:\n {list(self.E)}\n"
		result += f"Number of vertices: {self.n}\n"
		result += f"Number of edges: {self.m}\n"

		result +="__________________________________________"
		return result
#/*=====================================OPERATOR OVERLOADING=================================*/
	# DONE(Everton): Merge two or more MultiGraphs
	def __add__(*graphs):
		GraphClass = type(graphs[0])
		result = GraphClass({},{}) 	# empty MultiGraph
		for G in graphs:					# For each Graph we merge to the empty MultiGraph
			for v in G.V:
				result.add_vertice(v)
			for e in G.E:
				result.add_edge(e)
		return result

	# Indexation to get neighbours of vertice v
	# Ex: G[2] = neighbours of 2 in G
	def __getitem__(self,v):
		return self.neighbours(v)

	def __mul__(self, number:int or float):
		if self.weighted:
			for key in self.W:
				self.W[key] = self.W[key]*number
		return self

	def __rmul__(self, number:int or float):
		return self.__mul__(number)

	def __contains__(self, item):
		return item in self.v or item in self.E
#/*=====================================COMPARISONS=================================*/

	def __eq__(self, other): 
		CurrentClass = type(self) 
		if not isinstance(other, CurrentClass):
			# don't attempt to compare against unrelated types
			return NotImplemented
		equal_vertices = sorted(list(self.V)) == sorted(list(other.V))
		equal_edges 	= sorted(list(self.E)) == sorted(list(other.E))
		return equal_vertices and equal_edges
