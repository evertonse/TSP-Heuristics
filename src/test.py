from random import randint
from exgraph.graph 		import Graph
from exgraph.digraph 	import DiGraph
from exgraph.multidigraph import MultiDiGraph
from exgraph.multigraph import MultiGraph
from exgraph.algorithms import kruskal,prims
from ds.multiset import MultiSet as mset

import unittest  as ut

def test_multiset():
	m1 = mset([1,1,3,4])
	m2 = mset([1,1,4,4])
	m3 = mset([3,1,1,4])

	d = {
		m1:"sou m1",
		m2:"sou m2",
		m3:"sou m3"
	}
	print(d)

class TestGraph(ut.TestCase):
	def test_multigraph(self):
		n  = 12
		E = set()
		for i in range(n):
			for j in range(n):
				if i != j: # no self loops
					E.add((i,j, randint(n,2*n)) )
		G = MultiGraph(V={i for i in range(n)}, E=E,weighted=True)

		ok = True
		try:
			for e in G.E:
				w = G.weight(e)
			
			for v in G.V:
				G.neighbours(v)
			
			for e in list(G.E):
				G.remove_edge(e)
			
			for v in list(G.V):
				G.remove_vertice(v)
		except Exception as e:
			print(e)
			ok = False

		self.assertTrue(ok)

	def test_multidigraph(self):
		n  = 12
		E = set()
		for i in range(n):
			for j in range(n):
				E.add( (i,j, randint(n,2*n)) )
				E.add( (i,j, randint(n,2*n)) )
		G = MultiDiGraph(V={i for i in range(n)}, E=E,weighted=True)
		
		self.assertEqual(G.m,len(E))
		ok = True
		try:
			for e in G.E:
				w = G.weight(e)
			
			for v in G.V:
				G.neighbours(v)
			
			for e in list(G.E):
				G.remove_edge(e)
			
			for v in list(G.V):
				G.remove_vertice(v)
		except Exception as e:
			print(e)
			ok = False
		
		self.assertTrue(ok)

	def test_prim_kruskal(self):
		E = {
			(0,1, 10), (0,2, 1), (0,3, 4),
			(1,0, 10), (1,2, 3), (1,4, 0),
			(2,0, 1 ), (2,1, 3), (2,3, 2), (2,5, 8),
			(3,0, 4 ), (3,2, 2), (3,5, 2), (3,6, 7), 
			(4,1, 0 ), (4,5, 1), (4,7, 8), 
			(5,2, 8 ), (5,3, 2), (5,4, 1), (5,6, 6), (5,7, 9), 
			(6,3, 7 ), (6,5, 6), (6,7, 12), 
			(7,4, 8 ), (7,5, 9), (7,6, 12), 
		}
		G = Graph(V={i for i in range(8)}, E=E,weighted=True)

		self.assertTrue (
			len(list(E)) >= len( list(G.E) )
		)
		PT, Psum = prims(G) 
		KT, Ksum = kruskal(G)
		self.assertTrue(Psum==Ksum )


	def test_prims_kruskal_2(self):
		
		""""
		cd90 	ce120 	cf50 	ca140	 cb60
		bd120	be80	bf40	ba100	
		ad110	ae80	af90		
		fe60	fd90			
		ed50	
		"""			

		E = {
			('c','d', 90 ), ('c','e', 120), ('c','f',50), ('c','a', 140), ('c','b', 60),
			('b','d', 120), ('b','e', 80 ), ('b','f', 40),('b','a', 100),
			('a','d', 110), ('a','e', 80 ), ('a','f', 90),
			('f','e', 60),  ('f','d', 90 ), 
			('e','d', 50 ), 
		}
		G = Graph(V={'a','b','c','d','f','e'}, E=E,weighted=True)
		
		PT, Psum = prims(G) 
		KT, Ksum = kruskal(G)
		self.assertTrue(Psum==Ksum )

	def test_prim_kruskal_L4(self):

		E = {
			('BRA','BHO', 716 ),
			('CBA','BHO', 1594),('CBA','BRA', 1133), 
			('CTB','BHO', 1004),('CTB','BRA', 1366), ('CTB','CBA', 1679),
			('FOR','BHO', 2528),('FOR','BRA', 2200), ('FOR','CBA', 3406), ('FOR','CTB', 3541),
			('MAN','BHO', 3951),('MAN','BRA', 3490 ),('MAN','CBA', 2357 ),('MAN','CTB', 4036 ),('MAN','FOR', 5763 ), 
			('NAT','BHO', 2348),('NAT','BRA', 2422 ),('NAT','CBA', 3543 ),('NAT','CTB', 3365 ),('NAT','FOR', 537 ), ('NAT','MAN', 5985 ), 
			('POA','BHO', 1712),('POA','BRA', 2027 ),('POA','CBA', 2206 ),('POA','CTB', 711 ), ('POA','FOR', 4242 ),('POA','MAN', 4563 ),('POA','NAT', 4066), 
			('REC','BHO', 2061),('REC','BRA', 2135 ),('REC','CBA', 3255 ),('REC','CTB', 3231 ),('REC','FOR', 800 ), ('REC','MAN', 5698 ),('REC','NAT', 298 ),('REC','POA', 3779 ), 
			('RJO','BHO', 439), ('RJO','BRA', 1148 ),('RJO','CBA', 2017 ),('RJO','CTB', 852 ), ('RJO','FOR', 2826 ),('RJO','MAN', 4374 ),('RJO','NAT', 2625),('RJO','POA', 1553 ),('RJO','REC', 2338), 
			('SAL','BHO', 1372),('SAL','BRA', 1446 ),('SAL','CBA', 2566 ),('SAL','CTB', 2385 ),('SAL','FOR', 1389 ),('SAL','MAN', 5009 ),('SAL','NAT', 1131),('SAL','POA', 3090 ),('SAL','REC', 897 ), ('SAL','RJO', 1678 ), 
			('SPO','BHO', 586), ('SPO','BRA', 1015 ),('SPO','CBA', 1614 ),('SPO','CTB', 408 ), ('SPO','FOR', 3127 ),('SPO','MAN', 3971 ),('SPO','NAT', 2947),('SPO','POA', 1109 ),('SPO','REC', 2660 ),('SPO','RJO', 429 ), ('SPO','SAL', 1962 ), 
		}
		G = DiGraph(V={}, E=E,weighted=True)
		
		self.assertEqual(G.m, len(E))

		vertices_from_edges = set()
		edges_from_edges = list()
		for u,v, w in E:
			edges_from_edges.append((u,v))
			vertices_from_edges.add(u)
			vertices_from_edges.add(v)
		
		self.assertEqual( G.m, len(edges_from_edges))
		self.assertEqual( G.n, len(vertices_from_edges))
		self.assertEqual( sorted(list(G.V)), sorted(list(vertices_from_edges)) )
		PT, Psum = prims(G) 
		KT, Ksum = kruskal(G)
		self.assertTrue(Psum==Ksum )


	if __name__ == '__main__':
		ut.main()