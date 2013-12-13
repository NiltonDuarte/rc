from graph_tool.all import *
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
		
	def influenciaConjunta(self, degree):
		"""retorna a media de grau dos vertices apontados pelos vertices mais influentes da rede,
		vertices influentes serao os vertices com in-degree alto"""
		
		"""Eigenvector centrality
			Focuses on the connections of neighbours
			Reveals vertices that are well connected
			
			How well is this vertice connected to other well connected people"""
		
		sumNeighbours = 0;
		sumDegree = 0;
		vertexInfluenceList = []
		
		for v in self.g.vertices():
			vertexDegree = v.in_degree()
			if vertexDegree > degree:
				vertexNeighbours = 0
				vertexNeighboursDegree = 0
				for neighbour in v.out_neighbours():
					neighbourDegree = neighbour.in_degree()
					vertexNeighbours +=1
					vertexNeighboursDegree += neighbourDegree
				vertexInfluenceList.append(vertexNeighboursDegree/vertexNeighbours if vertexNeighbours > 0 else 0)
				sumNeighbours += vertexNeighbours
				sumDegree += vertexNeighboursDegree
			
		print vertexInfluenceList									#nao da no mesmo
		print sum(vertexInfluenceList) / len(vertexInfluenceList)	#media das medias
		return sumDegree/sumNeighbours								#media entre todos
																		
		
		
		

fileName = sys.argv[1]
dirName = './'+sys.argv[1][:-4]
if not os.path.exists(dirName):
	os.makedirs(dirName)

o = rcGraph(fileName)
o.g.list_properties()

print(o.g)


