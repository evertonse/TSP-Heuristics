
## Implementação de 5 heuristicas para TSP:
Foram implementadas as heuristicas : 
	Bellmore & Nemhauser, 
	Twice-Around,
	Christofides,
	Insere Vértice 1
	e Insere Vértice 2

IMPORTANTE: Na implementação do  Christofides, foi utilizado uma library apenas especificamente na parte do 'matching perfeito'.
	Fora isso, todo o resto foi feito inteiramente por mim.

## Código:
Separo abaixo entre pastas, textos e arquivos interessantes para essa implementação.

#### Pastas:

"src"    : Todo o código e textos então nesas pasta <\br>
"data"	 : Os dados da base de dado e serialização do grafos
"exgraph": As implementações dos Grafos, DiGrafos, MultiGrafos, além de algums algortimos uteis como 'hierholzer' e 'prims'
"ds"	 : Estrutura de dados auxiliares

#### Textos:
"TSP Heuristic Tours Info {nome da heuristica}.txt" : Ciclos encontrados, informações sobre tempo de excução, custos e outras info.
	
#### Arquivos:
"tspheuristics.py" : Algoritmos implementados para cada Heuristica
"tspgraphs.py"	   : Coleta e serialização dos grafos retirados da base de dados fornecida.
"main.py"	   : Começo do programa
"utils.py" 	   : Funções uteis
	

## Artigo:
Basta abrir o file "Everton Santos de Andrade Júnior - Uso de Heuristicas para o Problema de TSP.pdf"
Contém detalhes da implementação, explicação teorica, tabela informando tempo de execução, complexidade computacional, e custos encontrados pelas heuristicas

## OBS:
Qualquer esclarecimento ou problemas, por favor fale comigo, email: evertonse.junior@gmail.com
