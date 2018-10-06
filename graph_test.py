from igraph import *

g = Graph.Erdos_Renyi(10,0.8,directed=False)
print g
plot(g)
g.delete_vertices((1, 3, 5, 7, 9))
print g
plot(g)