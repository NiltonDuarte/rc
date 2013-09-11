from graph_tool.all import *


class rcGraph:
	
	def __init__(self, fileName):
		self.g = load_graph(fileName)

	def drawGraph(self, fileName):
		graph_draw(self.g, vertex_text=self.g.vertex_index, vertex_font_size=8,output_size=(1000, 1000), output=fileName)


	def graphDegreeHistogram(self):
		vertexDegreeFrequencies = [0]*10

		for v in self.g.vertices():
			vertexDegree = v.out_degree()
			if len(vertexDegreeFrequencies) > vertexDegree:
				vertexDegreeFrequencies[vertexDegree] += 1
			
			else:
				for i in range(len(vertexDegreeFrequencies),vertexDegree+1):
					vertexDegreeFrequencies.append(0)
				vertexDegreeFrequencies[vertexDegree] += 1
				print "degree = ", vertexDegree

		print vertexDegreeFrequencies
		print max(vertexDegreeFrequencies)
		return vertexDegreeFrequencies

fileName = "mygraphML.xml"

g = rcGraph(fileName)
g.g.list_properties()
#print g.g.vertex(100).list_properties["_graphml_vertex_id"]
print(g.g)
