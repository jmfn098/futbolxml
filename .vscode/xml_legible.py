import xml.etree.ElementTree as ET
tree = ET.parse('deportes.futbol.eliminatorias.posiciones.xml')
root = tree.getroot()
print(root[10][0].text)
#for child in root :
#    for child2 in child :
#        print(child2.tag, child2.attrib)