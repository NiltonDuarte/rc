from finaltrabalho import *



fileName = "/home/nilton/workspace/rc/currSet.xml"
#dirName = './'+sys.argv[1][:-4]
#if not os.path.exists(dirName):
#	os.makedirs(dirName)

graph = rcGraph(fileName)
graph.g.list_properties()

print(graph.g)

initVertex = [56369, 64322]
probability = 1
totalSteps = 27
stepsEachTime = 25

print '@Params InitialVertex = '+str(initVertex) + ' InfectionProbability = ' + str(probability) + ' TotalSteps = ' + str(totalSteps) + ' StepsEachTime = ' + str(stepsEachTime) + '\n'

numberInfectedVerticesEachInstant, numberInfectedVerticesEachTime = graph.dinamicEpidemicProcess(initVertex, probability, totalSteps,stepsEachTime, False)

statsFile = open('niltonOutput.txt', 'a')

statsFile.write('@Params InitialVertex = '+str(initVertex) + ' InfectionProbability = ' + str(probability) + ' TotalSteps = ' + str(totalSteps) + ' StepsEachTime = ' + str(stepsEachTime) + '\n')
print "file wrote"
statsFile.write('numberInfectedVerticesEachInstant = ' + str(numberInfectedVerticesEachInstant) + '\n')
print "file wrote"
statsFile.write('numberInfectedVerticesEachTime = ' + str(numberInfectedVerticesEachTime) + '\n')
print "file wrote"

statsFile.close()

"""

GCCsizes = graph.dinamicGCCMetrics()

statsFile = open('GCCsizes.txt', 'w')
statsFile.write('intialTime = 126230461 timeInterval = 31536000 steps = 30 \n')
statsFile.write('GCC Sizes = ' + str(GCCsizes) + '\n')
print "file wrote"
statsFile.close()
"""
#graph.extractLargestCCErr("/home/nilton/workspace/rc/largestCC2k.xml.gz")


#comp, hist = label_components(graph.g)


#print comp.a
#print hist
