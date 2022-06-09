from exgraph.graph import Graph
from exgraph.multigraph 	import MultiGraph
from exgraph.algorithms import blossom, prims,hierholzer,greedy_matching


# Heuristica de Bellmore & Nemhauser
def bellmore_nemhauser(G:Graph): # O(n^2)
	# Começamos por qualquer vertice
	u = next(G.V)
	# Adicionamos o o ciclo hamiltoniano H
	H = [u]
	# enquanto não visitamos todos vertices
	while len(H) < G.n:
		min_weight 	= float("inf")
		min_vertice = -1
		# Escolhendo o vertice v cujo aresta (v,u) tem peso minimo
		for v in G.neighbours(u):
			if v in H:
				continue
			w = G.weight((u,v))
			if w < min_weight:
				min_weight 	= w
				min_vertice = v
		# adicionamos esse tal v
		H.append(min_vertice)
		# Trocamos u de lugar com esse tal v encontrado e repetimos o processo
		u = min_vertice
	H.append(H[0])
	
	return H

# Heuristica Twice around
def twice_around(G:Graph):
	# Ciclo hamiltoniano H a ser encontrados
	H = []
	# Encontramos M.S.T. T através de prims 
	T,_ = prims(G) 		 # O(|V|^2)
	
	# Duplicamos todos os arcos em T
	for u,v in list(T.E): # O(|E|)
		w = T.weight((u,v))
		T.add_edge((v,u,w))

	# Encontranmos um cliclo euleriano
	L = hierholzer(T) 	# O(|E|)

	# TW a parte de remoção de vertices duplos
	while L:					# O(|E|)
		l = L.pop()
		if l not in H:
			H.append(l)

	# retornamos para o começo, formando um ciclo
	H.append(H[0])
	return H

# Heuristica christofides
def christofides(G:Graph):
	# Ciclo hamiltoniano H a ser encontrados
	H = []
	T = MultiGraph({},{},"MST", weighted=True)
	# Encontramos M.S.T. T através de prims 
	prims(G,MST=T) 		 # O(|V|^2)
	
	# Grafo que terá todos os vertices impáres de T 
	odd = Graph({},{},name="ODD", weighted=True)
	
	for t in T.V:
		# checangem de vertices de grau impar
		if T.deg(t) % 2  != 0:
			odd.add_vertice(t)
	# Transformamos 'odd' em um grafo completo
	for v in odd.V:
		for u in odd.V:
			if u != v:
				w = G.weight((u,v))
				odd.add_edge((u,v,w))
	
	#M = greedy_matching(odd)
	
	# Através do algoritimo vendorizado de Edmonds utilizando o  conceito de blossom
	# encontramos um Matching M de custo minimo
	M = blossom(odd)

	# A quantidade de edges nesse matching desse ser igual a exatamente metade da quantidade de vertices de odd
	# pois odd é completo e peso teorema de hand shaking em T sabemos que odd deve ter nº de vertices even 
	assert(len(M) == odd.n//2)

	# Fazemos T = (T.V , T.E ⋃ M) 
	for e in M:
		u,v,w = e
		T.add_edge((u,v,w))

	# Encontranmos um cliclo euleriano
	L = hierholzer(T) 	# O(|E|)

	# TW removemos vertices repetidos
	while L:					# O(|E|)
		l = L.pop()
		if l not in H:
			H.append(l)
	
	H.append(H[0])
	return H

def insert_vertice_1(G:Graph):
	# Seja H um ciclo inicial qualquer
	H = list(G.V)[:3]
	H.append(H[0])

	while len(H) != G.n+1:
		k = -1
		min_weight = float("inf") 
		for v in H:
			for u in G.neighbours(v):
				w = G.weight((v,u))
				if w <  min_weight and u not in H:
					min_weight = w
					k = u

		insert_best = float("inf")
		insert_at = -1
		for i in range(len(H)-1):
			insert_cost = G.weight((H[i],k)) + G.weight((k,H[i+1])) - G.weight((H[i],H[i+1])) 
			if insert_cost < insert_best:
				insert_best = insert_cost
				insert_at = i +1
		H.insert(insert_at,k)
	return H

def insert_vertice_2(G:Graph):
	H = list(G.V)[:3]
	H.append(H[0])

	while len(H) != G.n+1:
		insert_best = float("inf")
		insert_at = -1
		
		for k in (v for v in  G.V if v not in H):
			for i in range(len(H)-1):
				insert_cost = G.weight((H[i],k)) + G.weight((k,H[i+1])) - G.weight((H[i],H[i+1])) 
				if insert_cost < insert_best:
					insert_best = insert_cost
					insert_at = i +1
		
		H.insert(insert_at,k)
	return H