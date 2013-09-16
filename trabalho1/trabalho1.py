from graph_tool.all import *
import matplotlib.pyplot as plot
import numpy
import scipy.misc as spy


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
		
	def plotHistogram(self, histogram, numbins, xlabel, ylabel, title):
		"""Funcao para plot do Histograma"""
		n, bins, patches = plot.hist(histogram, numbins)
		plot.xlabel(xlabel)
		plot.ylabel(ylabel)
		plot.title(title)
		plot.show()

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
		"""Retorna média de dada propriedade do vértice, como grau ou clusterizacao"""
		return vertex_average(self.g, prop)
		
	def vertexHistogram(self, direction):
		"""Retorna histograma de grau de vertices"""
		return vertex_hist(self.g,direction)
		
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
		"""Retorna coeficiente de clusterizacao global do grafo, utilizando métrica
			dos slides"""
		globalClust = 0
		for coef in localClusArray:
			globalClust += coef
		return globalClust/self.g.num_vertices()
		
	def globalGraphClustering(self):
		"""Retorna coeficiente de clusterizacao global do grafo por um metodo
			de triangularizacao"""
		return global_clustering(self.g)
		
	def influenciaConjunta(self, degree):
		"""retorna a media de grau dos vertices apontados pelos vertices mais influentes da rede,
		vertices influentes serao os vertices com in-degree alto"""
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
																		
		
		
		

fileName = "mygraphML.xml"

o = rcGraph(fileName)
o.g.list_properties()
#o.drawSFDPGraph("graph-draw-sfdp.png")
print(o.g)

degreeHist = o.vertexHistogram("in")
frequencyDegreeHist = o.degreeDistribution(degreeHist[0])
distanceHist = o.distanceHistogram()
diameterRelation = o.diameter()
frequencyDistanceHist = o.distanceDistribution(distanceHist)
localClust = o.localClustering()

#print degreeHist
#print frequencyDegreeHist
#print distanceHist
#print frequencyDistanceHist
#print (vertex_average(o.g, localClust))

#print o.influenciaConjunta(20)

vertexAverage = o.averageVertexProp("in")
averageLocalClustering = o.averageVertexProp(localClust)
globalClust = o.globalClustering(localClust.a)
print 'Iniciando global clustering'
globalClustCoef = o.globalGraphClustering()
print 'Fim de global clustering'

print 'Graph density = ', o.graphDensity()
print 'Degree average = ', vertexAverage[0], ' +- ', vertexAverage[1]
print 'Average distance = ', o.averageDistance(distanceHist)
print 'Diameter = ', diameterRelation[0], ' | Source = ', o.g.vertex_properties['_graphml_vertex_id'][diameterRelation[1][0]],' | Target = ', o.g.vertex_properties['_graphml_vertex_id'][diameterRelation[1][1]]
print 'Average local clustering = ', averageLocalClustering[0], ' +- ', averageLocalClustering[1]
print 'Global Graph clustering = ', globalClustCoef[0], ' +- ', globalClustCoef[1]
print 'Global clustering = ', globalClust

#Plots ruins com grafos mal distribuidos
o.plotHistogram(degreeHist, 50, 'n de Vertices', 'Grau', 'Grau de vertices')
o.plotHistogram(frequencyDegreeHist, 50, 'P[D=k]', 'Grau', 'Distribuicao de grau')
o.plotHistogram(frequencyDistanceHist, 50, 'Frequencia de distancia', 'Distancia', 'Distribuicao de distancia')
o.plotHistogram(localClust.a, 50, 'Coeficiente de clusterizacao local', 'Vertices', 'Distribuicao de clusterizacao')


"""Bar plot
fqHist.append(0)
plot.bar(dgHist[1], fqHist, align='center')
plot.show()
"""



#dummy = katz(o.g)
#graph_draw(o.g,output="test_katz.png")
#pos = fruchterman_reingold_layout(o.g, n_iter=1000)
#graph_draw(o.g, pos=pos, output="graph-draw-fr.png")
