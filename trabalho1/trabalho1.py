from graph_tool.all import *


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
	
	def diameter(self):
		distance, source_target = pseudo_diameter(self.g)
		return distance, source_target
		
	def vertexHistogram(self, direction):
		return vertex_hist(self.g,direction)
		
	def distanceHistogram(self):
		return distance_histogram(self.g)
		
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
			
		print vertexInfluenceList
		print sum(vertexInfluenceList) / len(vertexInfluenceList)
		return sumDegree/sumNeighbours
					
		
		
		

fileName = "mygraphML.xml"

o = rcGraph(fileName)
o.g.list_properties()
#o.drawSFDPGraph("graph-draw-sfdp.png")
print(o.g)
print o.vertexHistogram("in")
print o.influenciaConjunta(20)




#dummy = katz(o.g)
#graph_draw(o.g,output="test_katz.png")
#pos = fruchterman_reingold_layout(o.g, n_iter=1000)
#graph_draw(o.g, pos=pos, output="graph-draw-fr.png")
