from finaltrabalho import *
#fileName = "./dataset/dblb946684800.xml"
fileName = "./dataset/currSet.xml"
#dirName = './'+sys.argv[1][:-4]
#if not os.path.exists(dirName):
#	os.makedirs(dirName)



rcg = rcGraph(fileName)

"""
distanceList, degreeHistList, frequencyDegreeHistList = rcg.dinamicGCCMetrics1()
rcg.writeList(distanceList,"dblp946684800","distanceList")
rcg.writeList(degreeHistList,"dblp946684800","degreeHistList")
rcg.writeList(frequencyDegreeHistList,"dblp946684800","frequencyDegreeHistList")

localClustList, localClustHistList rcg.dinamicGCCMetrics2() 
rcg.writeList(localClustList,"dblp946684800","localClustList")
rcg.writeList(localClustHistList,"dblp946684800","localClustHistList")
"""
centralityTupleList, centralityHistList, centralityList, majorCentralityList = rcg.dinamicGCCMetrics3()
rcg.writeList(centralityTupleList,"dblp946684800","centralityTupleList")
rcg.writeList(centralityHistList,"dblp946684800","centralityHistList")
rcg.writeList(centralityList,"dblp946684800","centralityList")
rcg.writeList(majorCentralityList,"dblp946684800","majorCentralityList")

