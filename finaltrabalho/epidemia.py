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
	def dinamicEpidemicProcess(self, initVertexID = 1, infectionProbability = 1, stepsTotal = 10,  stepsEachTime = 3, intialTime = 126230461, timeInterval = 31536000):
		"""
		@timeInterval = 31536000 is one year
		@initialTime = 126230461 is 01 / 01 / 74 @ 12:01:01am UTC
		"""
		currTime = intialTime
		infectedVertices = [] #all time
		infectedVerticesThisTime = [] #infected vertices in this time iteration
		randomNumber = 0
		numInfectedVertices = 1
		numberInfectedVerticesEachInstant = []
		numberInfectedVerticesEachTime = []
		
		vertex = self.g.vertex(initVertexID)
		infectedVertices.append(vertex)
		self.infectionProp[vertex] = True
		#print self.g.vertex_index[vertex]
		#print self.g.vertex_properties['_graphml_vertex_id'][vertex]
		totalStep = 0
		while totalStep < stepsTotal:
			totalStep += 1
			infectedVerticesThisTime = list(infectedVertices)
			infectecVerticesNow = numInfectedVertices #how many infected vertices now
			numberInfectedVerticesEachTime.append(infectecVerticesNow) #store the number of infected vertices
			print "time step ", totalStep
			currTime += timeInterval
			timeStep = 0
			while timeStep < stepsEachTime:
				timeStep += 1
				instInfectedVertices = list(infectedVerticesThisTime) #uma copia da lista de vertices infectados neste instante
				infectecVerticesNow = numInfectedVertices #how many infected vertices now
				numberInfectedVerticesEachInstant.append(infectecVerticesNow) #store the number of infected vertices
				print "infectecVerticesNow =",infectecVerticesNow, " vertices na lista =", len(instInfectedVertices)
				if infectecVerticesNow == self.g.num_vertices():
					print "broke"
					break
				
				#para cada vertice infectado
				for infectedVertex in instInfectedVertices:	
					numNeighbour = 0
					numNeighbourInfected = 0
					#para cada vertice vizinho de um infectado
					for edgeNeighbour in infectedVertex.all_edges():
						if self.g.edge_properties["time"][edgeNeighbour] < currTime:
							numNeighbour += 1
							numNeighbourInfected += 1
							#se nao esta infectado
							edgeTarget = edgeNeighbour.target()
							edgeSource = edgeNeighbour.source()
							if self.infectionProp[edgeTarget] == False:
								numNeighbourInfected -= 1
								randomNumber = random()
								#se passou pela chance de ser infectado
								if randomNumber < infectionProbability:
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
								if randomNumber < infectionProbability:
									#vertice eh infectado e adicionado na lista de infectados
									infectedVertices.append(edgeSource)
									infectedVerticesThisTime.append(edgeSource)
									self.infectionProp[edgeSource] = True
									numInfectedVertices += 1
									numNeighbourInfected += 1
					if numNeighbour == numNeighbourInfected:
						infectedVerticesThisTime.remove(infectedVertex)
							
		return numberInfectedVerticesEachInstant, numberInfectedVerticesEachTime