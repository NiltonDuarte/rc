import xml.etree.ElementTree as ET
import string
import sys

"""
<graphml>
	<graph id="G" edgedefault="undirected">
		<node id="n10"/>
		<edge source="n0" target="n2"/>
     </graph>
</graphml>
"""

outFileName = sys.argv[2]
inFileName = sys.argv[1]

inFile = open(inFileName)
print inFile

graphmlET = ET.Element('graphml')
graphmlET.set('xmlns','http://graphml.graphdrawing.org/xmlns')
graphmlET.set('xmlns:xsi','http://www.w3.org/2001/XMLSchema-instance')
graphmlET.set('xsi:schemaLocation','http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd')
datakeyET = ET.SubElement(graphmlET,'key')
datakeyET.set('id','d0')
datakeyET.set('for', 'edge')
datakeyET.set('attr.name', 'time')
datakeyET.set('attr.type', 'int')
graphET = ET.SubElement(graphmlET,'graph')
graphET.set('id', 'G')
graphET.set('edgedefault','directed')
try:
	nodeList = [];
	nodesAdded = 0;
	edgesAdded = 0;
	for line in inFile:
		if '%' in line:
			print "Line deleted !" + line
		else:
			line = line.strip()
			lineInfos = line.split(' ')
			if lineInfos[0] not in nodeList:
				nodeET = ET.SubElement(graphET,'node')
				nodeET.set('id',lineInfos[0])
				nodeList.append(lineInfos[0])
				nodesAdded += 1
			if lineInfos[1] not in nodeList:
				nodeET = ET.SubElement(graphET,'node')
				nodeET.set('id',lineInfos[1])
				nodeList.append(lineInfos[1])
				nodesAdded +=1
			edgeET = ET.SubElement(graphET,'edge')
			edgeET.set('source',lineInfos[0])
			edgeET.set('target',lineInfos[1])
			dataET = ET.SubElement(edgeET, 'data')
			dataET.set('key','d0')
			dataET.text = str(lineInfos[4])
			edgesAdded += 1
			
	print "Nodes added = ",nodesAdded
	print "Edges added = ", edgesAdded
					
finally:
	inFile.close()		

tree = ET.ElementTree(graphmlET)
#tree.write(outFileName +".graphml", encoding="UTF-8", xml_declaration=True)
tree.write(outFileName +".xml", encoding="UTF-8", xml_declaration=True)
