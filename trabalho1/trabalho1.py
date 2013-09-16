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
		
	def plotHistogram(self, histogram, xlabel, ylabel, title):
		n, bins, patches = plot.hist(histogram, 50)
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
	
	def diameter(self):
		distance, source_target = pseudo_diameter(self.g)
		return distance, source_target
		
	def averageVertexDegree(self, direction):
		return vertex_average(self.g, direction)
		
	def vertexHistogram(self, direction):
		return vertex_hist(self.g,direction)
		
	def distanceHistogram(self):
		return distance_histogram(self.g)
		
	def degreeDistribution(self, degreeList):
		degreeFrequency = []
		for degree in range(len(degreeList)):
			frequency = degreeList[degree] / self.g.num_vertices()
			degreeFrequency.append(frequency)
		return degreeFrequency
		
	def averageDistance(self, histogram):
		dTotal = 0
		dAverage = 0
		for i in range(len(histogram[0])):
			dTotal+= histogram[0][i]*histogram[1][i]
		comb = spy.comb(self.g.num_vertices(), 2)
		dAverage = dTotal/comb
		return dAverage
	
	def distanceDistribution(self, histogram):
		comb = spy.comb(self.g.num_vertices(), 2)
		distanceFrequency = []
		for distance in histogram[1][1:]:
			distanceFrequency.append(histogram[0][distance-1]/comb)
		return distanceFrequency
		
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
#print degreeHist
#print frequencyDegreeHist
#print distanceHist
print frequencyDistanceHist

#print o.influenciaConjunta(20)

vertexAverage = o.averageVertexDegree("in")
print 'Degree average = ', vertexAverage[0], ' +- ', vertexAverage[1]
print 'Average distance = ', o.averageDistance(distanceHist)
print 'Diameter = ', diameterRelation[0], ' | Source = ', o.g.vertex_properties['_graphml_vertex_id'][diameterRelation[1][0]],' | Target = ', o.g.vertex_properties['_graphml_vertex_id'][diameterRelation[1][1]]

#Plots ruins com grafos mal distribuidos
o.plotHistogram(degreeHist, 'n de Vertices', 'Grau', 'Grau de vertices')
o.plotHistogram(frequencyDegreeHist, 'P[D=k]', 'Grau', 'Distribuicao de grau')
o.plotHistogram(frequencyDistanceHist, 'Frequencia de distancia', 'Distancia', 'Distribuicao de distancia')


"""Bar plot
fqHist.append(0)
plot.bar(dgHist[1], fqHist, align='center')
plot.show()
"""



#dummy = katz(o.g)
#graph_draw(o.g,output="test_katz.png")
#pos = fruchterman_reingold_layout(o.g, n_iter=1000)
#graph_draw(o.g, pos=pos, output="graph-draw-fr.png")
