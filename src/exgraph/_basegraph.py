# _BaseGraph class, all operations are here

from typing import Any
from numpy import iterable
from sqlalchemy import false


class _BaseGraph():	
	@classmethod
	def empty(cls,*,name="empty"):
		return cls((),(),name=name)

	# for a _BaseGraph (DIRECTED _BaseGraph) ->
	# V = Vertices, E = Edges, n = # of vertices, if 
	def __init__(self,V,E,name="unnamed_graph",weights:dict[tuple,int]=None,multi=False,directed=False):
		if type(self) == _BaseGraph:
				raise Exception("<_BaseGraph> must be subclassed.")
		self._isdirected = directed
		if weights is not None:
			self._weights:dict[tuple,int] = weights
			self._isweighted = True
		else:
			self._isweighted = False
		self.name=name

		self._edges = set()
		"""utilizar listas de adjacências"""
		self._adj_list = {v:set() for v in V}	
		
		"""utilizar listas de predecessores"""
		self._pred_list = {v:set() for v in V}	
		
		for v in V:
			self.add_vertice(v)
		
		for e in E:
			if self.weighted:
				self.add_edge(tuple((e[0],e[1],self.weight(e))))
			else:
				self.add_edge(tuple(e))
			self.__add_pred_list(tuple(e))

	def __add_pred_list(self,e):
		u,w = tuple(e)
		if w not in self.V:
			self.add_vertice(w)
		if u not in self.V:
			self.add_vertice(u)
		self._pred_list[w].add(u)
	
	def __remove_pred_list(self,e):
		if e not in self._edges:
			return
		self._pred_list[e[1]].remove(e[0])

	"""inserir arestas"""
	# e = 2-tuple (u,v) \in E
	def add_edge(self,e):
		if e[0] not in self.V:
			self.add_vertice(e[0])
		if e[1] not in self.V:
			self.add_vertice(e[1])

		# Because is directed we must NOT add vice-versa
		# Must only add once
		self._edges.add((e[0],e[1]))
		self._adj_list[e[0]].add(e[1])
		self.__add_pred_list((e[0],e[1]))
		if self.weighted:
			self.update_weight((e[0],e[1]),e[2])

	"""inserir vértices"""
	def add_vertice(self,v):
		if v not in self._adj_list.keys():
			self._adj_list[v] = set()
			self._pred_list[v] = set()

	"""remover arestas"""
	def remove_edge(self,edge):
		e = tuple(edge)
		if e not in self._edges:
			return
		if self.weighted:
			del(self.W[(e[0],e[1])])
		self._edges.remove((e[0],e[1]))

		self._adj_list[e[0]].remove(e[1])
		self.__remove_pred_list(e)
		assert(e[1] not in self._adj_list[e[0]])


	""""remover vértices"""
	def remove_vertice(self,v):
		#for u in list(self.neighbours(v)):
		#	e = (u,v)
		#	self.remove_edge(e)
		#	self.__remove_pred_list(e)
		#	assert(v not in self._adj_list[u])
		#	if self.weighted:
		#		del(self.W[(u,v)])
		if v not in self.V:
			return
		for u in list(self.predecessors(v)):
			e = (u,v)
			self.remove_edge(e)
			self.__remove_pred_list(e)
			assert(v not in self._adj_list[u])
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
				C.add_edge((*e,self.weight(e)))
			else:
				C.add_edge(e)
		return C

	def save(self,filepath=None):
		from pickle import dump
		filepath = filepath if filepath is not None else self.name
		with open(filepath, 'wb') as f:
			dump(self,f)
	
	def load(filepath=None):
		from pickle import load
		with open(filepath, 'rb') as f:
			G = load(f)
		return G

	def weight(self,e) -> int or Any:
		if e not in self._weights: 
			return None
		if self.weighted:
			return self._weights[e]
		else:
			return 1

	def distance(self,p:iterable):
		if not self.weighted: return len(p)
		total = 0
		for i in range(len(p)-1):
			e = (p[i],p[i+1])
			total += self.weight(e)
		return total
					
	def update_weight(self,e,w):
		if self.weighted:
			self._weights[e] = w

	@property
	def weighted(self):
		return self._isweighted
		
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
	
	@property 
	def isdirected(self):
		return self._isdirected
	
	@property 
	def isweighted(self):
		return self._isweighted

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
	def __str__(self, sort=False,slim=True):
		return f"G(|V| = {self.n},|E| ={self.m})" 
	def __repr__(self, sort=False,slim=True):
		V = list(self.V)
		if sort == True:
			ordered = sorted
			V = sorted(list(self.V))
		else:
			ordered = lambda x:x		
		result =f"__________________{self.name}_______________________\n"
		if self.weighted:
			result += f"{self.name}\nGraph-Type Wheighted:{type(self)}\n"
		else:
			result += f"{self.name}\nGraph-Type:{type(self)}\n"
		
		for v in V:
			if self.weighted:
				result += f"{v}->{ordered([f'{u}|{self.W[(v,u)]}' for u in list(self.neighbours(v))])}"+ "\n"
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
	# DONE(Everton): Merge two or more _BaseGraphs
	def __add__(*Graphs):
		result = _BaseGraph({},{}) 	# empty _BaseGraph
		for G in Graphs:					# For each Graph we merge to the empty _BaseGraph
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
