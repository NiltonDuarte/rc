from graph_tool.all import *
import matplotlib.pyplot as plot
import numpy
import scipy.misc as spy
import sys
import os
from random import *

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
		self.infectionProp = self.g.new_vertex_property("bool")
		self.timeIntervalProp = self.g.new_edge_property("bool")
		self.gcc = self.extractGCC()
			
	def drawGraph(self, fileName):
		graph_draw(self.g,output_size=(1000, 1000), output=fileName)#, vertex_text=self.g.vertex_index, vertex_font_size=8)
		
	def drawARFGraph(self, fileName):
		pos = arf_layout(self.g, max_iter=0)
		graph_draw(self.g, pos=pos, output=fileName)
		
	def drawSFDPGraph(self, fileName):
		pos = sfdp_layout(self.g)
		graph_draw(self.g, pos=pos, output=fileName)
		
	def drawEpidemicGraph(self, fileName):
		graph_draw(self.gcc, vertex_fill_color=self.infectionProp, output=fileName)

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
		
	#returns a property map with informs if the edge is in(1) or out(0) The time interval specified
	def isOnInterval(self, end, start = 0):
		timePropertyMap = self.g.edge_properties["time"]
		edgeOnTimeIntervalProp = self.g.new_edge_property("bool") 
		for e in self.g.edges():	
			if ( (timePropertyMap[e] > start) and (timePropertyMap[e] < end) ):
				edgeOnTimeIntervalProp[e] = True
			else:
				edgeOnTimeIntervalProp[e] = False
		
		self.timeIntervalProp = edgeOnTimeIntervalProp
		return edgeOnTimeIntervalProp
		
	def setEdgeFilter(self, prop = "time"): #to reset, use None as argument.
		if (prop == "time"): #default argument set timeIntervalProp as filtering property
			self.g.set_edge_filter(self.timeIntervalProp)
			return
		
		self.g.set_edge_filter(prop)
		return
	def saveLargestCC(self, outFileName="largestCC.xml.gz"):# extract the largest component as a graph returns, and saves it
		l = label_largest_component(self.g)
		u = GraphView(self.g, vfilt=l)   
		u.save(outFileName)
		print ("Largest CC saved as " + outFileName)
		return
	
	def extractGCC(self):# extract the largest component as a graph returns, and saves it
		l = label_largest_component(self.g)
		u = GraphView(self.g, vfilt=l)
		return u
		
	def extractLargestCCErr(self, outFileName="largestCC.xml.gz"):# extract the largest component as a graph returns, and saves it
		l = label_largest_component(self.g)
		u = GraphView(self.g, vfilt=l)
		toRemove = []   
		for v in self.g.vertices():
			if(l[v] == False):
				toRemove.append(v)
		for v in toRemove:
			self.g.remove_vertex(v) 
		self.g.save(outFileName)
		print ("Largest CC saved as " + outFileName)
		return u
		
	#simulate an epidemic process on the network
	def epidemicProcess(self, initVertexID = 1, infectionProbability = 1, steps = 10):
		infectedVertices = []
		randomNumber = 0
		numInfectedVertices = 1
		numberInfectedVerticesEachInstant = []
		vertex = self.g.vertex(initVertexID)
		infectedVertices.append(vertex)
		self.infectionProp[vertex] = True
		#print self.g.vertex_index[vertex]
		#print self.g.vertex_properties['_graphml_vertex_id'][vertex]
		i = 0
		while i < steps:
			i += 1
			instInfectedVertices = list(infectedVertices) #uma copia da lista de vertices infectados neste instante
			infectecVerticesNow = numInfectedVertices #how many infected vertices now
			numberInfectedVerticesEachInstant.append(infectecVerticesNow) #store the number of infected vertices
			print "infectecVerticesNow =",infectecVerticesNow, " vertices na lista =", len(infectedVertices)
			if infectecVerticesNow == self.g.num_vertices():
				break
			
			#para cada vertice infectado
			for infectedVertex in instInfectedVertices:	
				numNeighbour = 0
				numNeighbourInfected = 0
				#para cada vertice vizinho de um infectado
				for neighbour in infectedVertex.all_neighbours():
					numNeighbour += 1
					numNeighbourInfected += 1
					randomNumber = random()
					#se nao esta infectado
					if self.infectionProp[neighbour] == False:
						numNeighbourInfected -= 1
						#se passou pela chance de ser infectado
						if randomNumber < infectionProbability:
							#vertice eh infectado e adicionado na lista de infectados
							infectedVertices.append(neighbour)   
							self.infectionProp[neighbour] = True
							numInfectedVertices += 1
							numNeighbourInfected += 1
				if numNeighbour == numNeighbourInfected:
					infectedVertices.remove(infectedVertex)
						
		return numberInfectedVerticesEachInstant
		
		#simulate an epidemic process on a dinamic network
	def dinamicEpidemicProcess(self, initVertexID = [1], infectionProbability = 1, stepsTotal = 10,  stepsEachTime = 3, saveImage = False, intialTime = 126230461, timeInterval = 31536000):
		"""
		@timeInterval = 31536000 is one year
		@initialTime = 126230461 is 01 / 01 / 74 @ 12:01:01am UTC
		"""
		currTime = intialTime
		infectedVertices = [] #all time
		infectedVerticesThisTime = [] #infected vertices in this time iteration
		randomNumber = 0
		numInfectedVertices = 0
		numberInfectedVerticesEachInstant = []
		numberInfectedVerticesEachTime = []
		
		for ID in initVertexID:
			numInfectedVertices += 1
			vertex = self.g.vertex(ID)
			infectedVertices.append(vertex)
			self.infectionProp[vertex] = True
		
		#print self.g.vertex_index[vertex]
		#print self.g.vertex_properties['_graphml_vertex_id'][vertex]
		totalStep = 0
		while totalStep < stepsTotal:
			totalStep += 1
			infectedVerticesThisTime = list(infectedVertices)
			infectecVerticesNow = len(infectedVertices) #numInfectedVertices #how many infected vertices now
			numberInfectedVerticesEachTime.append(infectecVerticesNow) #store the number of infected vertices
			print "time step ", totalStep
			currTime += timeInterval
			timeStep = 0
			while timeStep < stepsEachTime:
				timeStep += 1
				instInfectedVertices = list(infectedVerticesThisTime) #uma copia da lista de vertices infectados neste tempo
				infectecVerticesNow = len(infectedVertices) #numInfectedVertices #how many infected vertices now
				numberInfectedVerticesEachInstant.append(infectecVerticesNow) #store the number of infected vertices
				print "infectecVerticesNow =",infectecVerticesNow, " vertices na lista =", len(instInfectedVertices)
				
				#para cada vertice infectado
				for infectedVertex in instInfectedVertices:	
					numNeighbour = 0
					numNeighbourInfected = 0
					#para cada vertice vizinho de um infectado
					for edgeNeighbour in infectedVertex.all_edges():
						if self.g.edge_properties["time"][edgeNeighbour] < currTime:
							numNeighbour += 1
							numNeighbourInfected += 1
							
							edgeTarget = edgeNeighbour.target()
							edgeSource = edgeNeighbour.source()
							#se nao esta infectado
							if self.infectionProp[edgeTarget] == False:
								numNeighbourInfected -= 1
								randomNumber = random()
								#se passou pela chance de ser infectado
								if randomNumber <= infectionProbability:
									#vertice eh infectado e adicionado na lista de infectados
									infectedVertices.append(edgeTarget)
									infectedVerticesThisTime.append(edgeTarget)
									self.infectionProp[edgeTarget] = True
									numInfectedVertices += 1
									numNeighbourInfected += 1
							elif self.infectionProp[edgeSource] == False:
								numNeighbourInfected -= 1
								randomNumber = random()
								#se passou pela chance de ser infectado
								if randomNumber <= infectionProbability:
									#vertice eh infectado e adicionado na lista de infectados
									infectedVertices.append(edgeSource)
									infectedVerticesThisTime.append(edgeSource)
									self.infectionProp[edgeSource] = True
									numInfectedVertices += 1
									numNeighbourInfected += 1
					if numNeighbour == numNeighbourInfected:
						infectedVerticesThisTime.remove(infectedVertex)
							
		return numberInfectedVerticesEachInstant, numberInfectedVerticesEachTime
					
	def filterInfection(self):
		self.g.set_vertex_filter(self.infectionProp) #filtrar os vertices infectados
		
	def dinamicGCCMetrics(self, totalSteps = 25, intialTime = 126230461, timeInterval = 31536000):
		GCCsizes = []
		step = 0
		distanceList = []
		degreeHistList = []
		frequencyDegreeHistList = []
		localClustList = []
		localClustHistList = []
		centralityTupleList = []
		centralityHistList = []
		centralityList = []
		majorCentralityList = []
		
		currTime = intialTime
		while (step < totalSteps):
			print "step = ", step
			step += 1
			currTime += timeInterval
			self.setEdgeFilter(None)
			self.isOnInterval(currTime)
			print "intervalSet"
			self.setEdgeFilter("time")
			print "filsetSet"
			#gccVertices = self.extractGCC().num_vertices()
			#print gccVertices
			#GCCsizes.append(gccVertices)
			#distance
			distance, source_target = self.diameter()
			print "calculated distance"
			distanceList.append(distance)
			#degree hists
			degreeHist = self.vertexHistogram("total")
			print "calculated degreeHist"
			frequencyDegreeHist = self.degreeDistribution(degreeHist[0])
			print "calculated frequencyDegreeHist"
			degreeHistList.append(degreeHist)
			frequencyDegreeHistList.append(frequencyDegreeHist)
			#local clust
			localClust = self.localClustering()
			print "calculated localClust"
			localClustHist = vertex_hist(self.g, localClust, numpy.linspace(0,0.001,101))
			print "calculated localClustHist"
			localClustList.append(localClust)
			localClustHistList.append(localClustHist)
			#centrality
			centralityTuple = self.eigenvectorCentrality()
			print "calculated centralityTuple"
			centralityHist = vertex_hist(self.g, centralityTuple[1], numpy.linspace(0,0.5,101))
			print "calculated centralityHist"
			centrality = centralityTuple[1]
			majorCentrality = centralityTuple[0]
			centralityTupleList.append(centralityTuple)
			centralityHistList.append(centralityHist)
			centralityList.append(centrality)
			majorCentralityList.append(majorCentrality)
			
		print GCCsizes
		return distanceList, degreeHistList, frequencyDegreeHistList, localClustList, localClustHistList, centralityTupleList, centralityHistList, centralityList, majorCentralityList
		

	def dinamicGCCMetrics1(self, totalSteps = 25, intialTime = 126230461, timeInterval = 31536000):
		GCCsizes = []
		step = 0
		distanceList = []
		degreeHistList = []
		frequencyDegreeHistList = []
		localClustList = []
		localClustHistList = []
		centralityTupleList = []
		centralityHistList = []
		centralityList = []
		majorCentralityList = []
		
		currTime = intialTime
		while (step < totalSteps):
			print "step = ", step
			step += 1
			currTime += timeInterval
			self.setEdgeFilter(None)
			self.isOnInterval(currTime)
			print "intervalSet"
			self.setEdgeFilter("time")
			print "filsetSet"
			#gccVertices = self.extractGCC().num_vertices()
			#print gccVertices
			#GCCsizes.append(gccVertices)
			#distance
			distance, source_target = self.diameter()
			print "calculated distance"
			distanceList.append(distance)
			#degree hists
			degreeHist = self.vertexHistogram("total")
			print "calculated degreeHist"
			frequencyDegreeHist = self.degreeDistribution(degreeHist[0])
			print "calculated frequencyDegreeHist"
			degreeHistList.append(degreeHist)
			frequencyDegreeHistList.append(frequencyDegreeHist)
			
		return distanceList, degreeHistList, frequencyDegreeHistList
		
	def dinamicGCCMetrics2(self, totalSteps = 25, intialTime = 126230461, timeInterval = 31536000):
		GCCsizes = []
		step = 0
		distanceList = []
		degreeHistList = []
		frequencyDegreeHistList = []
		localClustList = []
		localClustHistList = []
		centralityTupleList = []
		centralityHistList = []
		centralityList = []
		majorCentralityList = []
		
		currTime = intialTime
		while (step < totalSteps):
			print "step = ", step
			step += 1
			currTime += timeInterval
			self.setEdgeFilter(None)
			self.isOnInterval(currTime)
			print "intervalSet"
			self.setEdgeFilter("time")
			print "filsetSet"
			#gccVertices = self.extractGCC().num_vertices()
			#print gccVertices
			#GCCsizes.append(gccVertices)
			#local clust
			localClust = self.localClustering()
			print "calculated localClust"
			localClustHist = vertex_hist(self.g, localClust, numpy.linspace(0,0.001,101))
			print "calculated localClustHist"
			localClustList.append(localClust)
			localClustHistList.append(localClustHist)

		return localClustList, localClustHistList
		
									
	def dinamicGCCMetrics3(self, totalSteps = 25, intialTime = 126230461, timeInterval = 31536000):
		GCCsizes = []
		step = 0
		distanceList = []
		degreeHistList = []
		frequencyDegreeHistList = []
		localClustList = []
		localClustHistList = []
		centralityTupleList = []
		centralityHistList = []
		centralityList = []
		majorCentralityList = []
		
		currTime = intialTime
		while (step < totalSteps):
			print "step = ", step
			step += 1
			currTime += timeInterval
			self.setEdgeFilter(None)
			self.isOnInterval(currTime)
			print "intervalSet"
			self.setEdgeFilter("time")
			print "filsetSet"
			#gccVertices = self.extractGCC().num_vertices()
			#print gccVertices
			#GCCsizes.append(gccVertices)

			#centrality
			centralityTuple = self.eigenvectorCentrality()
			print "calculated centralityTuple"
			centralityHist = vertex_hist(self.g, centralityTuple[1], numpy.linspace(0,0.5,101))
			print "calculated centralityHist"
			centrality = centralityTuple[1]
			majorCentrality = centralityTuple[0]
			centralityTupleList.append(centralityTuple)
			centralityHistList.append(centralityHist)
			centralityList.append(centrality)
			majorCentralityList.append(majorCentrality)
			
		return centralityTupleList, centralityHistList, centralityList, majorCentralityList
		
	def writeList(self, l, inputFileName="a"):
		f = open('distanceList_'+ inputFileName, 'w')
		for x in l:
			f.writelines(str(x))
			f.write('\n')
		f.close()

	
	def neigborsInfluence(self):
		x = []
		numDeCam2 = 0 #numero de caminhos comp 2
		for e in self.g.edges():
			numDeCam2 = 0
			for i in e.source().out_edges():
				if(e.target()==i.target()):
					continue
			for d in e.source().out_edges():
				if (d==e):
					continue
				for f in d.target().out_edges():
					if (d==f):
						continue
					if (f.target() == e.target()):
						#if(self.timeIntervalProp[f] < self.timeIntervalProp[e]):
							numDeCam2 += 1
			x.append([ self.g.vertex_index[e.source()], self.g.vertex_index[e.target()], numDeCam2])	
		print x			
		return 
						

		

		
"""
fileName = "./dataset/currSet.xml"
#dirName = './'+sys.argv[1][:-4]
#if not os.path.exists(dirName):
#	os.makedirs(dirName)

graph = rcGraph(fileName)
graph.g.list_properties()

print(graph.g)
graph.epidemicProcess()

prop = o.isOnInterval(o.g.edge_properties["time"] , 946684800, 1262304000)
print ("numero de arestas sem filtragem ", o.g.num_edges()) #numero de arestas sem filtragem
o.g.set_edge_filter(prop) #filtrar as arestas no intervalo
print ("numero de arestas apos filtragem ", o.g.num_edges())# numero de arestas apos filtragem
o.g.set_edge_filter(None) #limpar filtro
print ("numero de arestas apos limpeza de filtro ", o.g.num_edges())# numero de arestas apos limpeza de filtro
"""











