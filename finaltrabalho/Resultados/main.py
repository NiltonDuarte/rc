from finaltrabalho import *
fileName = "./dataset/dblb946684800.xml"
#fileName = "./dataset/currSet.xml"
#dirName = './'+sys.argv[1][:-4]
#if not os.path.exists(dirName):
#	os.makedirs(dirName)






rcg = rcGraph(fileName)

rcg.g = rcg.extractGCC()
print rcg.g.num_vertices()


bin_counts_hist_Degree, binRightEdges_hist_Degree, highestDegreeList,highestDegreesWithIndices, ccSizes = rcg.myMetrics()

rcg.writeList(bin_counts_hist_Degree,"dblp946684800","./result/bin_counts_hist_Degree")
rcg.writeList(binRightEdges_hist_Degree,"dblp946684800","./result/binRightEdges_hist_Degree")
rcg.writeList(highestDegreeList,"dblp946684800","./result/highestDegreeList")
rcg.writeList(highestDegreesWithIndices,"dblp946684800","./result/highestDegreesWithIndices")
rcg.writeList(ccSizes,"dblp946684800","./result/ccSizes")


"""
degreeHistList, frequencyDegreeHistList, diameter, averageDegree, GCCsizes = rcg.dinamicGCCMetrics1()
rcg.writeList(degreeHistList,"dblp946684800","./result/degreeHistList")
rcg.writeList(frequencyDegreeHistList,"dblp946684800","./result/frequencyDegreeHistList")
rcg.writeList(diameter,"dblp946684800","./result/diameter")
rcg.writeList(averageDegree,"dblp946684800","./result/averageDegree")
rcg.writeList(GCCsizes,"dblp946684800","./result/GCCsizes")

localClustList, localClustHistList, averageLocalClustList = rcg.dinamicGCCMetrics2() 
rcg.writeList(localClustList,"dblp946684800","./result/localClustList")
rcg.writeList(localClustHistList,"dblp946684800","./result/localClustHistList")
rcg.writeList(averageLocalClustList,"dblp946684800","./result/averageLocalClustList")

centralityTupleList, centralityHistList, centralityList, majorCentralityList = rcg.dinamicGCCMetrics3()
rcg.writeList(centralityTupleList,"dblp946684800","./result/centralityTupleList")
rcg.writeList(centralityHistList,"dblp946684800","./result/centralityHistList")
rcg.writeList(centralityList,"dblp946684800","./result/centralityList")
rcg.writeList(majorCentralityList,"dblp946684800","./result/majorCentralityList")
"""
