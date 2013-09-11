import xml.etree.ElementTree as ET
import string

"""
<graphml>
	<graph id="G" edgedefault="undirected">
		<node id="n10"/>
		<edge source="n0" target="n2"/>
     </graph>
</graphml>
"""

outFileName = "mygraphML"
inFileName = "Wiki-Vote.txt"

inFile = open(inFileName)
print inFile

graphmlET = ET.Element('graphml')
graphmlET.set('xmlns','http://graphml.graphdrawing.org/xmlns')
graphmlET.set('xmlns:xsi','http://www.w3.org/2001/XMLSchema-instance')
graphmlET.set('xsi:schemaLocation','http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd')
graphET = ET.SubElement(graphmlET,'graph')
graphET.set('id', 'G')
graphET.set('edgedefault','undirected')
try:
	nodeList = [];
	nodesAdded = 0;
	edgesAdded = 0;
	for line in inFile:
		if '#' in line:
			print "Line deleted !" + line
		else:
			line = line.strip()
			nodes = line.split('\t')
			if nodes[0] not in nodeList:
				nodeET = ET.SubElement(graphET,'node')
				nodeET.set('id',nodes[0])
				nodeList.append(nodes[0])
				nodesAdded += 1
			if nodes[1] not in nodeList:
				nodeET = ET.SubElement(graphET,'node')
				nodeET.set('id',nodes[1])
				nodeList.append(nodes[1])
				nodesAdded +=1
			edgeET = ET.SubElement(graphET,'edge')
			edgeET.set('source',nodes[0])
			edgeET.set('target',nodes[1])
			edgesAdded += 1
	print "Nodes added = ",nodesAdded
	print "Edges added = ", edgesAdded
					
finally:
	inFile.close()		

tree = ET.ElementTree(graphmlET)
tree.write(outFileName +".graphml", encoding="UTF-8", xml_declaration=True)
tree.write(outFileName +".xml", encoding="UTF-8", xml_declaration=True)
