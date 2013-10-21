from graph_tool.all import *
from operator import itemgetter
import matplotlib.pyplot as plot
import numpy
import scipy.misc as spy
import sys
import os

class matPlot:
	
	def __init__(self, numbins):
		self.numbins = numbins
		
	def plotHistogram(self, histogram, xlabel, ylabel, title):
		"""Funcao para plot do Histograma"""
		n, bins, patches = plot.hist(histogram, self.numbins)
		plot.xlabel(xlabel)
		plot.ylabel(ylabel)
		plot.title(title)
		plot.show()
		
	def writeHistogram(self, histogram, fileName):
		"""Escreve em arquivo dados para plot"""
		fileHist = open(fileName, 'w')
		for element in zip(histogram[0], histogram[1]):
			fileHist.write(str(element[0])+'\t'+str(element[1])+'\n')
		fileHist.close()


class rcGraph:
	
	def __init__(self, fileName):
		self.g = load_graph(fileName)

	def drawGraph(self, fileName):
		graph_draw(self.g,output_size=(1000, 1000), output=fileName)#, vertex_text=self.g.vertex_index, vertex_font_size=8)
		
	def drawARFGraph(self, fileName):
		pos = arf_layout(self.g, max_iter=0)
		graph_draw(self.g, pos=pos, output=fileName)
		
	def drawSFDPGraph(self, fileName):
		pos = sfdp_layout(self.g)
		graph_draw(self.g, pos=pos, output=fileName)

	""" funcao obsoleta
	def degreeHistogram(self):
		vertexDegreeFrequencies = [0]*10

		for v in self.g.vertices():
			vertexDegree = v.in_degree()
			if len(vertexDegreeFrequencies) > vertexDegree:
				vertexDegreeFrequencies[vertexDegree] += 1
			
			else:
				for i in range(len(vertexDegreeFrequencies),vertexDegree+1):
					vertexDegreeFrequencies.append(0)
				vertexDegreeFrequencies[vertexDegree] += 1
				print "degree = ", vertexDegree
		return vertexDegreeFrequencies
	"""
	def graphDensity(self):
		"""Retorna densidade do grafo"""
		n = self.g.num_vertices()
		m = self.g.num_edges()
		return (2.0*m)/(n*(n-1.0))
	
	def diameter(self):
		"""Retorna diametro do grafo"""
		distance, source_target = pseudo_diameter(self.g)
		return distance, source_target
		
	def averageVertexProp(self, prop):
		"""Retorna media de dada propriedade do vertice, como grau ou clusterizacao"""
		return vertex_average(self.g, prop)
		
	def vertexHistogram(self, direction):
		"""Retorna histograma de grau de vertices"""
		return vertex_hist(self.g, direction)
		
	def distanceHistogram(self):
		"""Retorna histograma de distancias entre vertices"""
		return distance_histogram(self.g)
		
	def degreeDistribution(self, degreeList):
		"""Distribuicao de grau de vertices, probabilidade de grau igual a k"""
		degreeFrequency = []
		for degree in range(len(degreeList)):
			frequency = degreeList[degree] / self.g.num_vertices()
			degreeFrequency.append(frequency)
		return degreeFrequency
		
	def averageDistance(self, histogram):
		"""Retorna media da distancia entre vertices"""
		dTotal = 0
		dAverage = 0
		for i in range(len(histogram[0])):
			dTotal+= histogram[0][i]*histogram[1][i]
		comb = spy.comb(self.g.num_vertices(), 2)
		dAverage = dTotal/comb
		return dAverage
	
	def distanceDistribution(self, histogram):
		"""Retorna distribuicao de distancias, frequencia relativa"""
		comb = spy.comb(self.g.num_vertices(), 2)
		distanceFrequency = []
		for distance in histogram[1][1:]:
			distanceFrequency.append(histogram[0][distance-1]/comb)
		return distanceFrequency
		
	def localClustering(self):
		"""Retorna coeficiente de clusterizacao local"""
		return local_clustering(self.g, undirected=False)
	
	def globalClustering(self, localClusArray):
		"""Retorna coeficiente de clusterizacao global do grafo, utilizando metrica
			dos slides"""
		globalClust = 0
		for coef in localClusArray:
			globalClust += coef
		return globalClust/self.g.num_vertices()
		
	def globalGraphClustering(self):
		"""Retorna coeficiente de clusterizacao global do grafo por um metodo
			de triangularizacao"""
		return global_clustering(self.g)
		
	def eigenvectorCentrality(self):
		return eigenvector(self.g)
		
#############################Trabalho 2#################################
# centralidade de grau, betweeness, closeness, autovalor, katz, Pagerank.
#Para cada rede, faca uma tabela com os 10 vertices mais centrais em cada metrica. O que voce pode concluir?
#Para cada rede, faca uma tabela com os 10 vertices menos centrais em cada metrica. O que voce pode concluir?
#Para cada rede, calcule a correlacao entre vizinhos utilizando como caracteristica cada uma das metricas de centralidade. 
#    Por exemplo, qual eh a correlacao da centralidade de Pagerank entre vertices vizinhos? O que voce pode concluir? 

	#def eigenvectorCentrality(self):
	
	def degreeCentrality(self):
		n = self.g.num_vertices()
		centralityList = []
		print len(centralityList)
		for v in self.g.vertices():
			vertexDegree = v.in_degree()
			vertexCentrality = float(vertexDegree)/(n-1)
			vertexID = self.g.vertex_properties['_graphml_vertex_id'][v]
			centralityList.append((vertexID, vertexCentrality))
		return centralityList
	
	def betweenessCentrality(self):
		return betweenness(self.g)
	
	def closenessCentrality(self):
		return closeness(self.g)
		
	def katzCentrality(self):
		return katz(self.g)
		
	def pageRankCentrality(self):																		
		return pagerank(self.g)
		
	def relateListElements(self, propertyName):
		"""Retorna lista com id do Vertice e propriedade relacionados em uma tupla"""
		returnList = []
		for v in self.g.vertices():
			prop = self.g.vertex_properties[propertyName][v]
			vertexID = self.g.vertex_properties['_graphml_vertex_id'][v]
			element = (vertexID, prop)
			returnList.append(element)
		return returnList
		
	def get10More(self, originalList):
		"""Retorna os 10 elementos maiores, relacionados com seus indices"""
		returnList = []
		sortedList = sorted(originalList, key=itemgetter(1))
		for i in range(10):
			centrality = sortedList.pop()
			returnList.append(centrality)
		return returnList
		

fileName = sys.argv[1]
dirName = './'+sys.argv[1][:-4]
if not os.path.exists(dirName):
	os.makedirs(dirName)

o = rcGraph(fileName)
o.g.list_properties()
centralityVertexList = o.degreeCentrality()
result = o.get10More(centralityVertexList)
centralityFile = open(dirName+'/centralidadeGrau.txt', 'w')
for i in range(len(result)):
	centralityFile.write("Vertex "+str(result[i][0])+"\t| Centrality = "+str(result[i][1])+"\n")
centralityFile.close()

centralityVertexMap,centralityEdgeMap = o.betweenessCentrality()
o.g.vertex_properties['betweeness'] = centralityVertexMap
centralitySet = o.relateListElements('betweeness')
result = o.get10More(centralitySet)
centralityFile = open(dirName+'/centralidadeBetweeness.txt', 'w')
for i in range(len(result)):
	centralityFile.write("Vertex "+str(result[i][0])+"\t| Centrality = "+str(result[i][1])+"\n")
centralityFile.close()

centralityVertexMap = o.closenessCentrality()
o.g.vertex_properties['closeness'] = centralityVertexMap
centralitySet = o.relateListElements('closeness')
result = o.get10More(centralitySet)
centralityFile = open(dirName+'/centralidadeCloseness.txt', 'w')
for i in range(len(result)):
	centralityFile.write("Vertex "+str(result[i][0])+"\t| Centrality = "+str(result[i][1])+"\n")
centralityFile.close()

centralityVertexMap = o.katzCentrality()
o.g.vertex_properties['katz'] = centralityVertexMap
centralitySet = o.relateListElements('katz')
result = o.get10More(centralitySet)
centralityFile = open(dirName+'/centralidadeKatz.txt', 'w')
for i in range(len(result)):
	centralityFile.write("Vertex "+str(result[i][0])+"\t| Centrality = "+str(result[i][1])+"\n")
centralityFile.close()

centralityVertexMap = o.pageRankCentrality()
o.g.vertex_properties['pagerank'] = centralityVertexMap
centralitySet = o.relateListElements('pagerank')
result = o.get10More(centralitySet)
centralityFile = open(dirName+'/centralidadePageRank.txt', 'w')
for i in range(len(result)):
	centralityFile.write("Vertex "+str(result[i][0])+"\t| Centrality = "+str(result[i][1])+"\n")
centralityFile.close()


#print o.g.vertex_properties[]
#o.drawSFDPGraph("graph-draw-sfdp.png")
#print(o.g)

#degreeHist = o.vertexHistogram("in")
#frequencyDegreeHist = o.degreeDistribution(degreeHist[0])
#distanceHist = o.distanceHistogram()
#diameterRelation = o.diameter()
#frequencyDistanceHist = o.distanceDistribution(distanceHist)
#localClust = o.localClustering()
#localClustHist = vertex_hist(o.g, localClust, numpy.linspace(0,0.001,101))
#print localClustHist
#centralityTuple = o.eigenvectorCentrality()
#centralityHist = vertex_hist(o.g, centralityTuple[1], numpy.linspace(0,0.5,101))
#print centralityHist
#centrality = centralityTuple[1]
#majorCentrality = centralityTuple[0]

#graph_draw(o.g, output_size=(1000, 1000), vertex_color=centrality, vertex_fill_color=centrality, vertex_size=1, edge_pen_width=0, output="centrality"+fileName[:-4]+".png")


#print degreeHist
#print frequencyDegreeHist
#print distanceHist
#print frequencyDistanceHist
#print (vertex_average(o.g, localClust))
#print centrality.a

#print o.influenciaConjunta(20)

#vertexAverage = o.averageVertexProp("in")
#averageLocalClustering = o.averageVertexProp(localClust)
#globalClust = o.globalClustering(localClust.a)
#print 'Iniciando global clustering'
#globalClustCoef = o.globalGraphClustering()
#print 'Fim de global clustering'
"""
statsFile = open(dirName+'/stats.txt', 'w')

print 'Graph density = ', o.graphDensity()
statsFile.write('Graph density = '+str(o.graphDensity())+'\n')
print 'Degree average = ', vertexAverage[0], ' +- ', vertexAverage[1]
statsFile.write('Degree average = '+str(vertexAverage[0])+' +- '+str(vertexAverage[1])+'\n')
print 'Average distance = ', o.averageDistance(distanceHist)
statsFile.write('Average distance = '+str(o.averageDistance(distanceHist))+'\n')
print 'Diameter = ', diameterRelation[0], ' | Source = ', o.g.vertex_properties['_graphml_vertex_id'][diameterRelation[1][0]],' | Target = ', o.g.vertex_properties['_graphml_vertex_id'][diameterRelation[1][1]]
statsFile.write('Diameter = '+str(diameterRelation[0])+' | Source = '+str(o.g.vertex_properties['_graphml_vertex_id'][diameterRelation[1][0]])+' | Target = '+str(o.g.vertex_properties['_graphml_vertex_id'][diameterRelation[1][1]])+'\n')
print 'Average local clustering = ', averageLocalClustering[0], ' +- ', averageLocalClustering[1]
statsFile.write('Average local clustering = '+str(averageLocalClustering[0])+' +- '+str(averageLocalClustering[1])+'\n')
print 'Global Graph clustering = ', globalClustCoef[0], ' +- ', globalClustCoef[1]
statsFile.write('Global Graph clustering = '+str(globalClustCoef[0])+' +- '+str(globalClustCoef[1])+'\n')
print 'Global clustering = ', globalClust
statsFile.write('Global clustering = '+str(globalClust)+'\n')
print 'Major influence = ', majorCentrality
statsFile.write('Major influence = '+str(majorCentrality)+'\n')

statsFile.close()
"""

#pyplot = matPlot(11)
#pyplot.plotHistogram(localClustHist, 'Frequencia de coeficiente', 'Coeficiente', 'Coef de centralidade')
#pyplot.writeHistogram(localClustHist, dirName+'/coefClustHist.txt')
"""
#Plots ruins com grafos mal distribuidos
pyplot.plotHistogram(degreeHist, 'n de Vertices', 'Grau', 'Grau de vertices')
pyplot.writeHistogram(degreeHist[0], dirName+'/grauHist.txt')
pyplot.plotHistogram(frequencyDegreeHist, 'P[D=k]', 'Grau', 'Distribuicao de grau')
pyplot.writeHistogram(frequencyDegreeHist, dirName+'/grauDistrHist.txt')
pyplot.plotHistogram(frequencyDistanceHist, 'Frequencia de distancia', 'Distancia', 'Distribuicao de distancia')
pyplot.writeHistogram(frequencyDistanceHist, dirName+'/distDistrHist.txt')
pyplot.plotHistogram(localClust.a, 'Coeficiente de clusterizacao local', 'Vertices', 'Distribuicao de clusterizacao')
pyplot.writeHistogram(localClust.a, dirName+'/coefLocalClustHist.txt')
pyplot.plotHistogram(centrality.a, 'Coeficiente de centralidade', 'Vertices', 'Centralidade baseada em eigenvector')
pyplot.writeHistogram(centrality.a, dirName+'/coefCentralidadeHist.txt')
"""

"""Bar plot
fqHist.append(0)
plot.bar(dgHist[1], fqHist, align='center')
plot.show()
"""



#dummy = katz(o.g)
#graph_draw(o.g,output="test_katz.png")
#pos = fruchterman_reingold_layout(o.g, n_iter=1000)
#graph_draw(o.g, pos=pos, output="graph-draw-fr.png")
